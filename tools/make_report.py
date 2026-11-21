"""Builds the ~10-page final jury report as Report.docx (exported to PDF by Word).
Sections follow the faculty list: Title, Objective, Design Principles, Technical
model detail, Block Diagram, Flowchart, step-by-step screenshots of the working model."""
import os
from docx import Document
from docx.enum.section import WD_SECTION
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_BREAK
from docx.shared import Pt, Cm, Inches, RGBColor

ROOT = os.path.join(os.path.dirname(__file__), "..")
SHOT = os.path.join(ROOT, "screenshots", "steps")
DOCS = os.path.join(ROOT, "docs")

doc = Document()
for s in doc.sections:
    s.top_margin = s.bottom_margin = Cm(2.0)
    s.left_margin = s.right_margin = Cm(2.2)
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(12)
style.paragraph_format.space_after = Pt(4)
style.paragraph_format.line_spacing = 1.15
NAVY = RGBColor(0x1E, 0x3A, 0x8A)


def page_break():
    doc.add_paragraph().add_run().add_break(WD_BREAK.PAGE)


def h(text, size=16):
    p = doc.add_paragraph()
    r = p.add_run(text)
    r.bold = True
    r.font.size = Pt(size)
    r.font.color.rgb = NAVY
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(6)


def sub(text):
    h(text, 13)


def para(text):
    doc.add_paragraph(text)


def bullets(items, numbered=False):
    for it in items:
        doc.add_paragraph(it, style="List Number" if numbered else "List Bullet")


def picture(path, width, caption):
    doc.add_picture(path, width=Inches(width))
    doc.paragraphs[-1].alignment = WD_ALIGN_PARAGRAPH.CENTER
    c = doc.add_paragraph(caption)
    c.alignment = WD_ALIGN_PARAGRAPH.CENTER
    c.runs[0].italic = True
    c.runs[0].font.size = Pt(10)


def table(header, rows, widths=None):
    t = doc.add_table(rows=1, cols=len(header))
    t.style = "Light Grid Accent 1"
    for c, txt in zip(t.rows[0].cells, header):
        c.text = txt
    for row in rows:
        for c, txt in zip(t.add_row().cells, row):
            c.text = txt
    if widths:
        for row in t.rows:
            for c, w in zip(row.cells, widths):
                c.width = Cm(w)
    doc.add_paragraph()


# ---------------- Page 1: Title ----------------
for _ in range(4):
    doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("MIT ADT University, Pune\nSchool of Computing")
r.font.size = Pt(14)
r.bold = True
doc.add_paragraph()
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("LLM Mini Project Report")
r.font.size = Pt(16)
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
r = p.add_run("Resume Analyzer using a Large Language Model")
r.font.size = Pt(26)
r.bold = True
r.font.color.rgb = NAVY
p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
p.add_run("Problem Statement 41").font.size = Pt(14)
for _ in range(3):
    doc.add_paragraph()
info = doc.add_table(rows=0, cols=2)
info.style = "Light List Accent 1"
for k, v in [("Name", "Virendra Dilip Mahajan"), ("Roll No", "41"),
             ("Enrollment No", "ADT23SOCB1322"), ("Class", "LY Core 4"),
             ("GitHub", "github.com/Kmennn/llm-ps41-ADT23SOCB1322"),
             ("Project page", "kmennn.github.io/llm-ps41-ADT23SOCB1322")]:
    cells = info.add_row().cells
    cells[0].text, cells[1].text = k, v
page_break()

# ---------------- Page 2: Objective ----------------
h("1. Objective")
para("Final-year students send the same resume to many companies and rarely learn why they were "
     "rejected. Most companies first filter resumes with an applicant tracking system (ATS) that "
     "looks for the skills written in the job description (JD). If those skills are missing from the "
     "resume, a human never reads it.")
para("The objective of this project is to build a simple web tool that compares a student's resume "
     "with a job description and explains the gap in plain words, using a Large Language Model (LLM).")
sub("Specific goals")
bullets([
    "Accept a resume as a PDF and a job description as pasted text.",
    "Return a match score from 0 to 100.",
    "List the JD skills that the resume already shows (matched skills).",
    "List the JD skills that the resume does not show (missing skills), marking good-to-have ones.",
    "Give exactly 3 short, specific tips to improve the resume for this job.",
    "Run on a free, local open-source model, so no paid API key is needed.",
    "Never invent skills: use only facts written in the resume.",
])
sub("Scope")
para("The tool is for text-based PDF resumes in English. It does not rewrite the resume and does not "
     "read scanned (image) PDFs. It is a guide for the student, not a hiring decision.")
sub("Expected outcome")
para("A student uploads a resume, pastes a JD, clicks Analyze and within about 5 seconds sees the "
     "score, the two skill lists and the tips. Tested on 5 resume and JD pairs, the score should be "
     "high for a strong fit, middle for a partial fit and near zero for a wrong-field resume.")
page_break()

# ---------------- Page 3: Design principles ----------------
h("2. Design Principles")
table(["Principle", "How it is applied in this project"], [
    ("Keep it simple", "Two Python files only: app.py (UI, 50 lines) and analyzer.py (logic). One "
     "screen, one button. No database, no login."),
    ("Separation of concerns", "UI code (Streamlit) is kept apart from the logic (PDF reading, prompt, "
     "validation). The logic can be tested without the UI using tools/run_tests.py."),
    ("Grounded output, no hallucination", "The prompt tells the model to use only facts in the resume "
     "and never invent skills. Temperature is low (0.2) so answers are stable."),
    ("Structured output", "The model must reply with JSON with fixed keys, so the app can show the "
     "result reliably instead of parsing free text."),
    ("Never trust the model blindly", "Python checks every reply: the score is clamped to 0-100, only "
     "3 tips are kept, broken JSON triggers one retry, and an 'A or B' rule is enforced in code."),
    ("Model independence", "The code uses the OpenAI-compatible API, so the model can be swapped "
     "(local llama.cpp, Ollama, Groq or OpenAI) by changing 3 environment variables."),
    ("Privacy and zero cost", "The default model runs on our college GPU, so resumes are not sent to "
     "a third-party company and there is no API bill."),
    ("Clear feedback to the user", "Progress bar for the score, two columns for skills, numbered tips, "
     "and friendly messages for empty input or a scanned PDF."),
], widths=[4.5, 12])
sub("User interface design")
bullets([
    "Top: title and the name of the model being used, so the user knows what produced the answer.",
    "Middle: file upload (PDF/TXT) and a large text box for the job description.",
    "Bottom: the result. Score first (most important), then skills side by side, then tips.",
    "An expander shows the text read from the PDF, so the user can see what the model saw.",
])
page_break()

# ---------------- Pages 4-5: Technical model detail ----------------
h("3. Technical Model Detail")
sub("3.1 Technology stack")
table(["Layer", "Technology", "Purpose"], [
    ("Language", "Python 3.11", "All code"),
    ("User interface", "Streamlit 1.30+", "Web page: upload, text box, result view"),
    ("PDF reading", "PyPDF2 3.0", "Extract text from the resume PDF"),
    ("LLM client", "openai Python library", "Calls any OpenAI-compatible server"),
    ("LLM", "Qwen2.5-14B-Instruct, 4-bit GGUF (Q4_K_M)", "Compares resume and JD, writes JSON"),
    ("Model server", "llama.cpp llama-server (CUDA)", "Serves the model over HTTP"),
    ("Hardware", "NVIDIA RTX PRO 6000 GPU, Baramati AI lab", "Runs the model"),
    ("Testing", "tools/run_tests.py, Playwright", "5 test cases, screenshots"),
], widths=[3.2, 6.3, 7])
sub("3.2 Model details")
bullets([
    "Model: Qwen2.5-14B-Instruct by Alibaba Cloud, an open-weight instruction-tuned LLM with 14.7 "
    "billion parameters. It follows instructions well and is good at producing JSON.",
    "Quantization: Q4_K_M (about 4.5 bits per weight). The file is about 9 GB instead of about 29 GB, "
    "so it fits easily in GPU memory with only a small quality loss.",
    "Context window used: 8,192 tokens. The resume is cut to 12,000 characters and the JD to 6,000 "
    "characters, which keeps the input inside this window.",
    "Settings: temperature 0.2 (stable, less random answers).",
    "Speed: about 4 to 6 seconds per analysis on one GPU.",
    "Access: llama-server runs on a lab node; the app reaches it through an SSH tunnel on port 18141.",
])
sub("3.3 Prompt design")
para("The system prompt gives the model a role (strict technical recruiter and ATS), rules, and the "
     "exact JSON format. Main rules:")
bullets([
    "Use only facts written in the resume; a skill counts only if the resume clearly shows it.",
    "\"A or B\" in the JD is one requirement; matched if the resume has either one.",
    "Required skills decide most of the score; missing only good-to-have skills must not pull a "
    "strong fit below 80.",
    "Mark not-required missing skills with \"(good to have)\".",
    "Return only JSON with keys match_score, matched_skills, missing_skills, tips (exactly 3), summary.",
    "Scoring guide: 80-100 strong, 60-79 good, 40-59 partial, below 40 weak.",
])
para("The user message contains the resume text and the JD, clearly labelled RESUME and JOB DESCRIPTION.")
sub("3.4 Processing pipeline (analyzer.py)")
table(["Function", "What it does"], [
    ("read_resume(file)", "Reads every PDF page with PyPDF2 and joins the text. Also accepts .txt."),
    ("analyze(resume, jd)", "Checks both inputs, builds the messages, calls the LLM, retries once "
     "with 'reply with JSON only' if the answer is not valid JSON."),
    ("_parse_json(text)", "Finds the {...} block even if the model adds ``` fences or extra words."),
    ("_clean(result)", "Converts the score to an integer, clamps it to 0-100, keeps only 3 tips."),
    ("fix_or_alternatives()", "Finds 'A or B' pairs in the JD; if one is matched, removes the other "
     "from missing skills. This fixes a mistake the model still made after the prompt change."),
], widths=[4.5, 12])
sub("3.5 Output format")
para('{"match_score": 85, "matched_skills": ["Python", "Django", ...], "missing_skills": ["AWS", '
     '"Redis", "CI/CD (good to have)"], "tips": ["...", "...", "..."], "summary": "..."}')
page_break()

# ---------------- Page 6: Block diagram ----------------
h("4. Block Diagram")
picture(os.path.join(DOCS, "block_diagram.png"), 6.4, "Figure 1: Block diagram of the Resume Analyzer")
sub("Explanation of blocks")
bullets([
    "User: the student who uploads a resume and pastes a job description.",
    "Streamlit UI (app.py): the web page that takes the inputs and shows the result.",
    "PDF reader (PyPDF2): turns the resume PDF into plain text.",
    "Analyzer (analyzer.py): puts the resume text and the JD into the prompt.",
    "LLM server: Qwen2.5-14B on llama.cpp, running on the lab GPU, reached through an SSH tunnel "
    "using the OpenAI-compatible API. It returns JSON.",
    "Validator: parses the JSON, clamps the score, keeps 3 tips, retries once if needed and fixes "
    "'A or B' skills.",
    "Result view: score bar, matched and missing skills, 3 tips and a summary.",
])
page_break()

# ---------------- Page 7: Flowchart ----------------
h("5. Flowchart")
picture(os.path.join(DOCS, "flowchart.png"), 4.6, "Figure 2: Flowchart of one analysis")
para("The flowchart shows the three checks that keep the app from failing silently: empty input, a "
     "PDF with no text, and a reply that is not valid JSON (retried once).")
page_break()

# ---------------- Pages 8-9: Step-by-step screenshots ----------------
h("6. Working Model: Step-by-Step Screenshots")
para("All screenshots below are from one real run of the app on 21 Nov 2026, with the model running "
     "on the lab GPU. Sample resume: a fictional Python developer. Job description: Backend Developer "
     "(Fresher).")
steps = [
    ("step1_home.png", "Step 1: Open the app with 'streamlit run app.py'. The home screen shows the "
     "upload box and the job description box."),
    ("step2_empty_warning.png", "Step 2: Clicking Analyze with no input shows a warning instead of "
     "crashing (input check)."),
    ("step3_resume_uploaded.png", "Step 3: Upload the resume PDF (resume_python_dev.pdf)."),
    ("step4_jd_pasted.png", "Step 4: Paste the job description (Backend Developer, Fresher)."),
    ("step5_analyzing.png", "Step 5: Click Analyze. The spinner shows the resume is being read and the "
     "LLM is working."),
    ("step6_score.png", "Step 6: The match score (85/100) appears with a progress bar and a summary."),
    ("step7_skills_tips.png", "Step 7: Matched skills, missing skills (CI/CD marked good to have) and "
     "3 tips to improve."),
    ("step8_extracted_text.png", "Step 8: The expander shows the exact text read from the PDF, so the "
     "user can check what the model saw."),
]
# Two screenshots side by side, 4 per page. Side margins of the app are cropped.
from PIL import Image  # noqa: E402
CROP = os.path.join(ROOT, "tools", "_crops")
os.makedirs(CROP, exist_ok=True)
grid = doc.add_table(rows=0, cols=2)
for i in range(0, len(steps), 2):
    pics, caps = grid.add_row().cells, grid.add_row().cells
    for j in (0, 1):
        f, cap = steps[i + j]
        im = Image.open(os.path.join(SHOT, f))
        w, hgt = im.size
        out = os.path.join(CROP, f)
        im.crop((170, 0, min(w, 930), min(hgt, 840))).save(out)
        run = pics[j].paragraphs[0].add_run()
        run.add_picture(out, width=Inches(3.0))
        pics[j].paragraphs[0].alignment = WD_ALIGN_PARAGRAPH.CENTER
        cp = caps[j].paragraphs[0]
        cr = cp.add_run(cap)
        cr.italic = True
        cr.font.size = Pt(9.5)
page_break()

# ---------------- Page 10: Results, challenges, conclusion ----------------
h("7. Testing and Results")
table(["Resume", "Job description", "Expected", "Score", "Result"], [
    ("Python developer", "Backend developer", "strong", "85", "Correct"),
    ("Python developer", "Frontend (React)", "partial", "30", "Correct"),
    ("Data analyst", "Data analyst", "strong", "85", "Correct"),
    ("Data analyst", "ML engineer", "partial", "65", "Correct"),
    ("Mechanical engineer", "Backend developer", "weak", "0", "Correct"),
], widths=[3.6, 4, 2.4, 1.8, 2.4])
para("All 5 cases landed in the expected band. Each analysis took 4 to 6 seconds. Sample resumes are "
     "fictional and generated by tools/make_samples.py.")
h("8. Challenges and Fixes", 14)
bullets([
    "The model sometimes wrapped JSON in ``` fences. Fix: extract the {...} block and retry once.",
    "'Django or FastAPI': the model listed FastAPI as missing even when Django was present. Fix: "
    "prompt rule plus a Python check that removes the other option.",
    "A strong fit scored only 75 because good-to-have skills counted like required ones. Fix: a "
    "required vs good-to-have rule in the prompt; the score rose to 85.",
])
h("9. Conclusion and Future Scope", 14)
para("The Resume Analyzer gives a sensible score, clear skill lists and useful tips on a free, local "
     "open-source model, and the Python checks make the output reliable. Limitations: the free-text "
     "tips can still mention an alternative skill (for example FastAPI in Step 7), and scanned PDFs "
     "have no text to read. Future work: OCR (pytesseract) for scanned resumes, highlighting missing "
     "keywords inside the resume, and a hosted version with a public LLM API.")

doc.save(os.path.join(ROOT, "Report.docx"))
print("Report.docx written")
