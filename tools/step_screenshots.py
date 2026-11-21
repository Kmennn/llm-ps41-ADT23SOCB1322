"""Step-by-step screenshots of one real run for the report and PPT.
Needs the app running: streamlit run app.py --server.port 8541
Output: screenshots/steps/step1..step8.png"""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "screenshots", "steps")
os.makedirs(OUT, exist_ok=True)
URL = "http://localhost:8541"


def shot(page, name, full=False):
    page.wait_for_timeout(800)
    page.screenshot(path=os.path.join(OUT, name), full_page=full)
    print("saved", name)


with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1100, "height": 900})

    # Step 1: open the app
    page.goto(URL)
    page.wait_for_selector("text=Resume Analyzer")
    shot(page, "step1_home.png")

    # Step 2: click Analyze with nothing filled -> input check
    page.get_by_role("button", name="Analyze").click()
    page.wait_for_selector("text=Please upload a resume")
    shot(page, "step2_empty_warning.png")

    # Step 3: upload the resume PDF
    page.goto(URL)
    page.wait_for_selector("text=Resume Analyzer")
    page.set_input_files("input[type=file]", os.path.join(ROOT, "samples", "resume_python_dev.pdf"))
    page.wait_for_timeout(1500)
    shot(page, "step3_resume_uploaded.png")

    # Step 4: paste the job description
    page.fill("textarea", open(os.path.join(ROOT, "samples", "jd_backend_python.txt")).read())
    page.keyboard.press("Control+Enter")
    shot(page, "step4_jd_pasted.png")

    # Step 5: click Analyze -> LLM is working
    page.get_by_role("button", name="Analyze").click()
    page.wait_for_timeout(400)
    shot(page, "step5_analyzing.png")

    # Step 6-8: results
    page.wait_for_selector("text=Match score", timeout=120000)
    page.wait_for_timeout(1000)
    shot(page, "step6_score.png")
    # Streamlit scrolls inside its own container, so use a tall window and crop
    page.set_viewport_size({"width": 1100, "height": 2000})
    shot(page, "step7_full.png")
    page.get_by_text("Text extracted from your resume").click()
    page.wait_for_timeout(800)
    shot(page, "step8_full.png")
    browser.close()

from PIL import Image  # noqa: E402
Image.open(os.path.join(OUT, "step7_full.png")).crop((0, 560, 1100, 1400)).save(
    os.path.join(OUT, "step7_skills_tips.png"))
Image.open(os.path.join(OUT, "step8_full.png")).crop((0, 1100, 1100, 2000)).save(
    os.path.join(OUT, "step8_extracted_text.png"))
for f in ("step7_full.png", "step8_full.png"):
    os.remove(os.path.join(OUT, f))
