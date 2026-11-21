"""Core logic for PS41 Resume Analyzer: read a resume, compare it with a job
description using an LLM, and return a structured result."""
import json
import os
import re

from openai import OpenAI
from PyPDF2 import PdfReader

# Any OpenAI-compatible endpoint works. Default: Qwen2.5-14B-Instruct served
# by llama.cpp on a Baramati AI lab GPU (reached through an SSH tunnel).
BASE_URL = os.getenv("LLM_BASE_URL", "http://127.0.0.1:18141/v1")
API_KEY = os.getenv("LLM_API_KEY", "not-needed-for-local")
MODEL = os.getenv("LLM_MODEL", "qwen2.5-14b-instruct")

SYSTEM_PROMPT = """You are a strict technical recruiter and ATS (applicant tracking system).
Compare the RESUME with the JOB DESCRIPTION. Use ONLY facts written in the resume;
never invent skills. A skill counts as matched only if the resume clearly shows it.
Rules:
- "A or B" in the JD is ONE requirement: matched if the resume has either one.
  Never list the other option as missing.
- Required skills decide most of the score. "Good to have" skills add a little;
  missing only good-to-have skills must not pull a strong fit below 80.
- In missing_skills, add "(good to have)" after skills that are not required.

Return ONLY valid JSON, no extra text, with exactly these keys:
{
  "match_score": <integer 0-100>,
  "matched_skills": [<skills from the JD that the resume shows>],
  "missing_skills": [<skills the JD asks for that the resume does not show>],
  "tips": [<exactly 3 short, specific tips to improve the resume for this job>],
  "summary": "<2 sentences on overall fit>"
}
Scoring guide: 80-100 strong fit, 60-79 good, 40-59 partial, below 40 weak."""


def read_resume(file) -> str:
    """Extract text from an uploaded PDF (or a .txt) resume."""
    name = getattr(file, "name", str(file))
    if name.lower().endswith(".pdf"):
        reader = PdfReader(file)
        return "\n".join((page.extract_text() or "") for page in reader.pages).strip()
    data = file.read() if hasattr(file, "read") else open(file, "rb").read()
    return data.decode("utf-8", errors="ignore").strip()


def _parse_json(text: str) -> dict:
    """Models sometimes wrap JSON in ``` fences or add a sentence; keep the {...}."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.S)  # reasoning models
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError("The model did not return JSON:\n" + text[:300])
    return json.loads(match.group(0))


def _clean(result: dict) -> dict:
    score = int(float(result.get("match_score", 0)))
    return {
        "match_score": max(0, min(100, score)),
        "matched_skills": list(result.get("matched_skills", [])),
        "missing_skills": list(result.get("missing_skills", [])),
        "tips": list(result.get("tips", []))[:3],
        "summary": str(result.get("summary", "")),
    }


def fix_or_alternatives(result: dict, jd_text: str) -> dict:
    """The model sometimes ignores the "A or B" rule in the prompt, so check it
    in Python too: if the JD says "A or B" and either is matched, the other one
    is not missing."""
    pairs = re.findall(r"([\w.+#/-]+(?: [\w.+#-]+)?) or ([\w.+#/-]+)", jd_text)
    matched = {s.lower() for s in result["matched_skills"]}
    drop = set()
    for a, b in pairs:
        a, b = a.strip().lower(), b.strip().lower()
        a_last = a.split()[-1]
        if a in matched or a_last in matched:
            drop.add(b)
        if b in matched:
            drop.update({a, a_last})
    result["missing_skills"] = [
        s for s in result["missing_skills"]
        if s.lower().replace(" (good to have)", "") not in drop
    ]
    return result


def analyze(resume_text: str, jd_text: str, client=None) -> dict:
    if not resume_text.strip() or not jd_text.strip():
        raise ValueError("Both the resume and the job description are needed.")
    client = client or OpenAI(base_url=BASE_URL, api_key=API_KEY)
    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": f"RESUME:\n{resume_text[:12000]}\n\nJOB DESCRIPTION:\n{jd_text[:6000]}"},
    ]
    last_error = None
    for _ in range(2):  # one retry if the JSON is broken
        reply = client.chat.completions.create(model=MODEL, messages=messages, temperature=0.2)
        try:
            return fix_or_alternatives(_clean(_parse_json(reply.choices[0].message.content)), jd_text)
        except (ValueError, json.JSONDecodeError) as err:
            last_error = err
            messages.append({"role": "user", "content": "That was not valid JSON. Reply with the JSON object only."})
    raise ValueError(f"Could not get valid JSON from the model: {last_error}")
