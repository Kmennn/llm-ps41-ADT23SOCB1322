"""PS41 Resume Analyzer - web app for Vercel (Flask). Local run: python app.py
The LLM settings come from Vercel environment variables:
LLM_BASE_URL, LLM_MODEL, LLM_API_KEY."""
import io
import os
import sys

from flask import Flask, jsonify, request, send_from_directory

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from analyzer import MODEL, analyze, read_resume  # noqa: E402

app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = 5 * 1024 * 1024  # 5 MB upload limit
PUBLIC = os.path.join(os.path.dirname(os.path.abspath(__file__)), "web")


@app.get("/")
def home():
    return send_from_directory(PUBLIC, "index.html")


@app.get("/api/health")
def health():
    return jsonify({"ok": True, "model": MODEL})


@app.post("/api/analyze")
def analyze_route():
    # Preferred path: the browser extracts the PDF text (pdf.js) and sends JSON,
    # so the file itself never leaves the user's computer. Vercel's firewall
    # also blocked large multipart PDF uploads with a 403.
    if request.is_json:
        body = request.get_json(silent=True) or {}
        resume_text = str(body.get("resume_text") or "").strip()
        jd_text = str(body.get("jd") or "").strip()
        if not resume_text or not jd_text:
            return jsonify({"error": "Please upload a resume and paste a job description."}), 400
        try:
            result = analyze(resume_text[:12000], jd_text[:6000])
        except Exception as err:
            return jsonify({"error": f"Analysis failed: {err}"}), 502
        result["resume_text"] = resume_text[:3000]
        return jsonify(result)

    upload = request.files.get("resume")
    jd_text = (request.form.get("jd") or "").strip()
    if not upload or not jd_text:
        return jsonify({"error": "Please upload a resume and paste a job description."}), 400
    name = (upload.filename or "").lower()
    if not name.endswith((".pdf", ".txt")):
        return jsonify({"error": "Only PDF or TXT resumes are supported."}), 400
    buf = io.BytesIO(upload.read())
    buf.name = name
    try:
        resume_text = read_resume(buf)
        if not resume_text:
            return jsonify({"error": "No text found in the PDF. Is it a scanned image?"}), 400
        result = analyze(resume_text, jd_text)
    except Exception as err:  # shown to the user, like the Streamlit app
        return jsonify({"error": f"Analysis failed: {err}"}), 502
    result["resume_text"] = resume_text[:3000]
    return jsonify(result)


if __name__ == "__main__":
    app.run(port=8541, debug=True)
