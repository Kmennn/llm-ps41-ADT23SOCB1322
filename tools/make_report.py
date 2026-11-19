"""Builds the 2-page procedure report as Report.docx (exported to PDF by Word)."""
import os
from docx import Document
from docx.shared import Pt, Cm, Inches

ROOT = os.path.join(os.path.dirname(__file__), "..")
doc = Document()
for s in doc.sections:
    s.top_margin = s.bottom_margin = Cm(1.2)
    s.left_margin = s.right_margin = Cm(1.6)
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(12)
style.paragraph_format.space_after = Pt(0)


def h(text):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(13)
    p.paragraph_format.space_before = Pt(3)


def para(text):
    doc.add_paragraph(text)


def bullets(items, numbered=False):
    for it in items:
        doc.add_paragraph(it, style="List Number" if numbered else "List Bullet")


t = doc.add_paragraph()
r = t.add_run("Resume Analyzer using an LLM (PS 41)")
r.bold = True
r.font.size = Pt(16)
para("Name: Virendra Dilip Mahajan    Roll No: 41    Enrollment No: ADT23SOCB1322\n"
     "Class: LY Core 4    GitHub: https://github.com/Kmennn/llm-ps41-ADT23SOCB1322")

h("1. Problem statement")
para("Students apply for jobs without knowing why their resume is rejected. I built a tool that "
     "compares a resume with a job description (JD) and returns a match score, matched skills, "
     "missing skills and 3 tips. It helps final-year students tailor each resume before applying.")

h("2. Tools and model")
bullets([
    "Language and libraries: Python 3.11, Streamlit (UI), PyPDF2 (PDF text), openai client library.",
    "LLM: Qwen2.5-14B-Instruct (4-bit GGUF) served with llama.cpp llama-server on an NVIDIA RTX PRO "
    "6000 GPU in our college's Baramati AI lab, reached through an SSH tunnel. No paid API key is needed.",
    "The server speaks the OpenAI API format, so the same code runs with Groq, OpenAI or Ollama by "
    "changing three environment variables.",
])

h("3. Procedure")
bullets([
    "Started llama-server with the Qwen2.5-14B model on one lab GPU and opened an SSH tunnel to it.",
    "Wrote the prompt and tried it on sample inputs first.",
    "Wrote analyzer.py: read the resume PDF with PyPDF2, build the prompt with the resume and JD, call "
    "the LLM, extract and check the JSON (score clamped to 0-100, one retry if the JSON is broken).",
    "Built app.py in Streamlit: PDF upload, JD text box, Analyze button, score shown with st.progress, "
    "matched and missing skills in two columns, and the 3 tips.",
    "Made 3 fictional sample resumes and 5 JDs, ran 5 test cases (tools/run_tests.py) and took screenshots.",
    "Improved the prompt after the first test run (section 4) and added a Python check for \"A or B\" skills.",
], numbered=True)

h("4. Prompt used")
para("System prompt (short form): \"You are a strict technical recruiter and ATS. Compare the RESUME with "
     "the JOB DESCRIPTION. Use only facts written in the resume; never invent skills. 'A or B' in the JD "
     "is one requirement. Required skills decide most of the score; good-to-have skills add a little. "
     "Return only JSON with match_score (0-100), matched_skills, missing_skills, exactly 3 tips and a "
     "2-sentence summary.\" The user message holds the resume text and the JD.")
para("Change I made: in the first version the JD said \"Django or FastAPI\", but a resume with Django still "
     "got FastAPI listed as missing, and a resume with every required skill scored only 75 because "
     "good-to-have skills counted the same as required ones. I added the 'A or B' and required vs "
     "good-to-have rules. The score went from 75 to 85.")

h("5. Results")
tbl = doc.add_table(rows=1, cols=4)
tbl.style = "Light Grid Accent 1"
for c, txt in zip(tbl.rows[0].cells, ["Resume", "Job description", "Expected", "Score"]):
    c.text = txt
for row in [("Python developer", "Backend developer", "strong", "85"),
            ("Python developer", "Frontend (React)", "partial", "30"),
            ("Data analyst", "Data analyst", "strong", "85"),
            ("Data analyst", "ML engineer", "partial", "65"),
            ("Mechanical engineer", "Backend developer", "weak", "0")]:
    cells = tbl.add_row().cells
    for c, txt in zip(cells, row):
        c.text = txt
para("Each analysis took about 4-6 seconds on the lab GPU. Screenshot: Python developer resume against "
     "the backend JD (score 85, FastAPI correctly not listed as missing).")
doc.add_picture(os.path.join(ROOT, "tools", "report_result_crop.png"), width=Inches(4.6))

h("6. Challenges")
bullets([
    "The model sometimes wrapped JSON in ``` code fences. Fix: extract the {...} part with a regex and "
    "retry once with 'reply with JSON only' if it still fails.",
    "Even after the prompt change, the 14B model still listed FastAPI as missing. Fix: a small Python "
    "check that removes the other option of an 'A or B' pair when one of them is matched.",
    "Streamlit screenshots were cut off at the window height. Fix: took them with a taller window.",
])

h("7. Conclusion")
para("What works: PDF reading, a sensible score (strong fits 85, wrong-field resume 0), clear matched and "
     "missing skills, and specific tips, all on a free local model. What does not: the free-text tips "
     "can still mention an alternative skill, and scanned (image) PDFs have no text to read. Future "
     "improvement: add OCR (pytesseract) for scanned resumes and highlight missing keywords in the resume.")

doc.save(os.path.join(ROOT, "Report.docx"))
print("Report.docx written")
