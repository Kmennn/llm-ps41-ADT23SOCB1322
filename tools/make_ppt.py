"""Builds the final jury presentation: Presentation.pptx (16:9)."""
import os
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import PP_ALIGN

ROOT = os.path.join(os.path.dirname(__file__), "..")
SHOT = os.path.join(ROOT, "screenshots", "steps")
DOCS = os.path.join(ROOT, "docs")
NAVY, ACCENT, WHITE, DARK = RGBColor(0x1E, 0x3A, 0x8A), RGBColor(0x38, 0xBD, 0xF8), RGBColor(255, 255, 255), RGBColor(0x1F, 0x29, 0x37)

prs = Presentation()
prs.slide_width, prs.slide_height = Inches(13.333), Inches(7.5)
BLANK = prs.slide_layouts[6]
W, H = prs.slide_width, prs.slide_height


def rect(slide, x, y, w, h, color):
    s = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, x, y, w, h)
    s.fill.solid()
    s.fill.fore_color.rgb = color
    s.line.fill.background()
    return s


def text(slide, x, y, w, h, lines, size=20, color=DARK, bold=False, align=PP_ALIGN.LEFT, bullet=False):
    tb = slide.shapes.add_textbox(x, y, w, h)
    tf = tb.text_frame
    tf.word_wrap = True
    for i, line in enumerate(lines if isinstance(lines, list) else [lines]):
        p = tf.paragraphs[0] if i == 0 else tf.add_paragraph()
        p.text = ("•  " + line) if bullet else line
        p.alignment = align
        p.space_after = Pt(10)
        for r in p.runs:
            r.font.size = Pt(size)
            r.font.color.rgb = color
            r.font.bold = bold
            r.font.name = "Calibri"
    return tb


n = 0


def slide(title):
    global n
    n += 1
    s = prs.slides.add_slide(BLANK)
    rect(s, 0, 0, W, Inches(1.05), NAVY)
    rect(s, 0, Inches(1.05), W, Inches(0.06), ACCENT)
    text(s, Inches(0.5), Inches(0.18), Inches(11.5), Inches(0.8), title, 30, WHITE, True)
    text(s, Inches(11.6), Inches(7.0), Inches(1.5), Inches(0.4), str(n + 1), 12, RGBColor(0x64, 0x74, 0x8B), align=PP_ALIGN.RIGHT)
    text(s, Inches(0.5), Inches(7.0), Inches(8), Inches(0.4), "Resume Analyzer | PS 41 | Virendra Mahajan", 12, RGBColor(0x64, 0x74, 0x8B))
    return s


def pic(s, path, x, y, w=None, h=None):
    return s.shapes.add_picture(path, x, y, width=w, height=h)


# 1. Title
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, NAVY)
rect(s, 0, Inches(4.55), W, Inches(0.08), ACCENT)
text(s, Inches(0.8), Inches(1.2), Inches(11.7), Inches(0.6), "LLM Mini Project  |  Problem Statement 41", 22, ACCENT, True)
text(s, Inches(0.8), Inches(1.9), Inches(11.7), Inches(2.4), "Resume Analyzer using a Large Language Model", 50, WHITE, True)
text(s, Inches(0.8), Inches(4.9), Inches(11.7), Inches(1.8), [
    "Virendra Dilip Mahajan   |   Roll No 41   |   ADT23SOCB1322   |   LY Core 4",
    "MIT ADT University, Pune",
    "Live: resumeanalyzer-flax.vercel.app   |   github.com/Kmennn/llm-ps41-ADT23SOCB1322"], 20, WHITE)
LOGO_PNG = os.path.join(ROOT, "tools", "_crops", "logo.png")
if os.path.exists(LOGO_PNG):
    pic(s, LOGO_PNG, Inches(11.3), Inches(0.8), w=Inches(1.3))

# 2. Objective
s = slide("Objective")
text(s, Inches(0.6), Inches(1.4), Inches(12), Inches(1.2),
     "Students don't know why their resumes get rejected. Companies filter resumes with ATS software "
     "that looks for the skills in the job description.", 22)
text(s, Inches(0.6), Inches(2.7), Inches(12), Inches(4), [
    "Compare a resume (PDF) with a job description",
    "Give a match score from 0 to 100",
    "List matched skills and missing skills",
    "Give exactly 3 specific tips to improve",
    "Run on a free open-source LLM on our college GPU: no paid API",
    "Never invent skills: only facts written in the resume",
    "Usable by anyone from a public website"], 22, bullet=True)

# 3. Design principles
s = slide("Design Principles")
cards = [("Keep it simple", "One web page, one small Flask API (app.py), one logic file (analyzer.py)."),
         ("No hallucination", "Prompt: use only facts in the resume. Temperature 0.2."),
         ("Never trust blindly", "Python clamps score, keeps 3 tips, retries bad JSON, fixes 'A or B'."),
         ("Private by design", "Browser reads the PDF; only text is sent. Nothing is stored."),
         ("Secure", "Model needs a secret API key, reached over HTTPS only."),
         ("Free", "Open-source model on our college GPU. No API bill.")]
for i, (t, d) in enumerate(cards):
    x, y = Inches(0.6 + (i % 3) * 4.15), Inches(1.5 + (i // 3) * 2.75)
    c = rect(s, x, y, Inches(3.9), Inches(2.45), RGBColor(0xEF, 0xF6, 0xFF))
    rect(s, x, y, Inches(0.12), Inches(2.45), ACCENT)
    text(s, x + Inches(0.3), y + Inches(0.2), Inches(3.4), Inches(0.6), t, 22, NAVY, True)
    text(s, x + Inches(0.3), y + Inches(0.9), Inches(3.4), Inches(1.5), d, 17)

# 4. Technical model detail
s = slide("Technical Model Detail")
rows = [("Website", "HTML/CSS/JS page + Flask API on Vercel"), ("PDF reading", "pdf.js in the browser"),
        ("LLM", "Qwen2.5-14B-Instruct (14.7B params)"), ("Quantization", "Q4_K_M, about 9 GB"),
        ("Server", "llama.cpp llama-server, API key"), ("Hardware", "NVIDIA H200 slice, lab node 04"),
        ("Network", "Cloudflare HTTPS + SSH tunnels"), ("Settings", "temperature 0.2, 8K context"),
        ("Speed", "10-40 seconds per analysis")]
tbl = s.shapes.add_table(len(rows), 2, Inches(0.6), Inches(1.45), Inches(7.2), Inches(5.2)).table
tbl.columns[0].width, tbl.columns[1].width = Inches(2.2), Inches(5.0)
for r, (k, v) in enumerate(rows):
    for c, val in enumerate((k, v)):
        cell = tbl.cell(r, c)
        cell.text = val
        cell.text_frame.paragraphs[0].runs[0].font.size = Pt(17)
        cell.text_frame.paragraphs[0].runs[0].font.bold = c == 0
text(s, Inches(8.2), Inches(1.45), Inches(4.7), Inches(0.5), "Prompt rules", 22, NAVY, True)
text(s, Inches(8.2), Inches(2.0), Inches(4.7), Inches(4.8), [
    "Role: strict recruiter / ATS",
    "Only facts from the resume",
    "'A or B' = one requirement",
    "Required skills weigh most",
    "Reply ONLY in JSON",
    "Score guide: 80+ strong, below 40 weak"], 17, bullet=True)

# 5. Block diagram
s = slide("Block Diagram")
pic(s, os.path.join(DOCS, "block_diagram.png"), Inches(0.9), Inches(1.35), w=Inches(11.5))

# 6. Flowchart
s = slide("Flowchart")
pic(s, os.path.join(DOCS, "flowchart.png"), Inches(0.6), Inches(1.25), h=Inches(5.7))
text(s, Inches(5.6), Inches(1.8), Inches(7.2), Inches(5), [
    "Check 1: both inputs given, else show a warning",
    "Browser reads the PDF text with pdf.js",
    "Check 2: PDF has text, else 'scanned PDF' error",
    "Text goes to the Vercel API, which calls the model on node 04",
    "Check 3: reply is valid JSON, else ask again once",
    "Clean the result, then show score, skills and tips"], 20, bullet=True)

# 7-10. Step-by-step screenshots
steps = [("step1_home.png", "Step 1: Open the website"), ("step2_analyzer.png", "Step 2: The analyzer"),
         ("step3_empty_warning.png", "Step 3: Empty input gives a warning"), ("step4_resume_selected.png", "Step 4: Choose resume PDF"),
         ("step5_jd_pasted.png", "Step 5: Paste job description"), ("step6_analyzing.png", "Step 6: Analyze, live progress"),
         ("step7_result.png", "Step 7: Score 85/100, skills, tips"), ("step8_details.png", "Step 8: Text the model saw")]
for k in range(0, 8, 2):
    s = slide(f"Working Model: Steps {k + 1}-{k + 2}")
    for j in (0, 1):
        f, cap = steps[k + j]
        x = Inches(0.5 + j * 6.25)
        p = pic(s, os.path.join(SHOT, f), x, Inches(1.85), w=Inches(6.0))
        if p.height > Inches(4.9):
            ratio = Inches(4.9) / p.height
            p.height, p.width = Inches(4.9), int(p.width * ratio)
            p.left = int(x + (Inches(6.0) - p.width) / 2)
        p.line.color.rgb = RGBColor(0xCB, 0xD5, 0xE1)
        text(s, x, Inches(1.25), Inches(6.0), Inches(0.5), cap, 20, NAVY, True)

# 11. Results
s = slide("Testing and Results")
res = [("Resume", "Job description", "Expected", "Score"), ("Python developer", "Backend developer", "strong", "85"),
       ("Python developer", "Frontend (React)", "partial", "30"), ("Data analyst", "Data analyst", "strong", "85"),
       ("Data analyst", "ML engineer", "partial", "65"), ("Mechanical engineer", "Backend developer", "weak", "0")]
tbl = s.shapes.add_table(6, 4, Inches(0.8), Inches(1.6), Inches(11.7), Inches(3.9)).table
for r, row in enumerate(res):
    for c, val in enumerate(row):
        cell = tbl.cell(r, c)
        cell.text = val
        cell.text_frame.paragraphs[0].runs[0].font.size = Pt(20)
text(s, Inches(0.8), Inches(5.8), Inches(11.7), Inches(1), "All 5 cases in the expected band. 10-40 seconds each on the live site.", 22, NAVY, True)

# 12. Challenges
s = slide("Challenges and Fixes")
text(s, Inches(0.6), Inches(1.5), Inches(12), Inches(5.3), [
    "JSON wrapped in ``` fences  ->  extract the {...} block, retry once",
    "'Django or FastAPI': FastAPI wrongly listed missing  ->  prompt rule + Python check",
    "Strong fit scored only 75  ->  required vs good-to-have rule: score now 85",
    "Vercel can't run Streamlit  ->  rebuilt as web page + Flask API",
    "Vercel firewall blocked a 461 KB PDF (403)  ->  browser reads PDF, sends text",
    "Lab GPU has no public address  ->  key-protected Cloudflare tunnel"], 21, bullet=True)

# 13. Conclusion
s = slide("Conclusion and Future Scope")
text(s, Inches(0.6), Inches(1.4), Inches(6), Inches(0.6), "What works", 24, NAVY, True)
text(s, Inches(0.6), Inches(2.0), Inches(6), Inches(4.5), [
    "Sensible scores: 85 strong, 0 wrong field", "Clear matched / missing skills",
    "Specific tips", "Live public website, free and private"], 20, bullet=True)
text(s, Inches(6.9), Inches(1.4), Inches(6), Inches(0.6), "Next steps", 24, NAVY, True)
text(s, Inches(6.9), Inches(2.0), Inches(6), Inches(4.5), [
    "OCR for scanned PDFs", "Highlight missing keywords in the resume",
    "Fixed tunnel address + custom domain", "Tips can still mention an alternative skill"], 20, bullet=True)

# 14. Thank you
s = prs.slides.add_slide(BLANK)
rect(s, 0, 0, W, H, NAVY)
text(s, 0, Inches(2.6), W, Inches(1.2), "Thank you", 60, WHITE, True, PP_ALIGN.CENTER)
text(s, 0, Inches(4.0), W, Inches(1), "Questions?   |   resumeanalyzer-flax.vercel.app", 22, ACCENT, align=PP_ALIGN.CENTER)

prs.save(os.path.join(ROOT, "Presentation.pptx"))
print("Presentation.pptx written,", len(prs.slides), "slides")
