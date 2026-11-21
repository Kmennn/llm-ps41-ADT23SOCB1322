"""Step-by-step screenshots of one real run on the live Vercel site.
Output: screenshots/steps/step1..step8.png"""
import os
import sys
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(__file__), "..")
OUT = os.path.join(ROOT, "screenshots", "steps")
os.makedirs(OUT, exist_ok=True)
URL = sys.argv[1] if len(sys.argv) > 1 else "https://resumeanalyzer-flax.vercel.app"


def save(target, name):
    target.screenshot(path=os.path.join(OUT, name))
    print("saved", name)


with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1280, "height": 800})
    page.goto(URL)
    page.wait_for_timeout(2500)
    page.evaluate("document.querySelectorAll('.rv').forEach(e=>{e.style.transition='none';e.classList.add('in')})")

    # Step 1: landing page
    save(page, "step1_home.png")

    app = page.locator(".app")
    page.locator("#analyze").scroll_into_view_if_needed()
    page.wait_for_timeout(500)
    # Step 2: analyzer, empty
    save(app, "step2_analyzer.png")

    # Step 3: Analyze with nothing filled -> input check
    page.click("#go")
    page.wait_for_timeout(500)
    save(page.locator("#form"), "step3_empty_warning.png")

    # hide the sticky nav for element shots and clear the warning
    page.add_style_tag(content=".nav{display:none!important}")
    page.evaluate("document.getElementById('msg').className='msg'")

    # Step 4: choose the resume PDF
    page.set_input_files("#resume", os.path.join(ROOT, "samples", "resume_python_dev.pdf"))
    page.wait_for_timeout(500)
    save(page.locator("#form"), "step4_resume_selected.png")

    # Step 5: paste the job description (sample button)
    page.click("[data-jd=backend]")
    page.wait_for_timeout(300)
    save(page.locator("#form"), "step5_jd_pasted.png")

    # Step 6: Analyze -> progress while the model works
    page.click("#go")
    page.wait_for_timeout(2500)
    save(app, "step6_analyzing.png")

    # Step 7-8: result
    page.wait_for_selector("#res", state="visible", timeout=120000)
    page.wait_for_timeout(1500)
    out = page.locator(".out")
    save(out, "step7_result.png")
    page.click("#res summary")
    page.wait_for_timeout(400)
    save(page.locator("#res"), "step8_details.png")
    browser.close()
