"""Drives the running Streamlit app (port 8541) with real inputs and saves
full-page screenshots of the results."""
import os
from playwright.sync_api import sync_playwright

ROOT = os.path.join(os.path.dirname(__file__), "..")
CASES = [
    ("resume_python_dev.pdf", "jd_backend_python.txt", "1_python_dev_vs_backend.png"),
    ("resume_data_analyst.pdf", "jd_ml_engineer.txt", "2_data_analyst_vs_ml.png"),
    ("resume_mechanical.pdf", "jd_backend_python.txt", "3_mechanical_vs_backend.png"),
]
with sync_playwright() as p:
    browser = p.chromium.launch(channel="chrome", headless=True)
    page = browser.new_page(viewport={"width": 1100, "height": 1750})
    page.goto("http://localhost:8541")
    page.wait_for_selector("text=Resume Analyzer")
    page.screenshot(path=os.path.join(ROOT, "screenshots", "0_home.png"), full_page=True)
    for resume, jd, shot in CASES:
        page.goto("http://localhost:8541")
        page.wait_for_selector("text=Resume Analyzer")
        page.set_input_files("input[type=file]", os.path.join(ROOT, "samples", resume))
        page.wait_for_timeout(1500)
        page.fill("textarea", open(os.path.join(ROOT, "samples", jd)).read())
        page.keyboard.press("Control+Enter")
        page.get_by_role("button", name="Analyze").click()
        page.wait_for_selector("text=Match score", timeout=120000)
        page.wait_for_timeout(1000)
        page.screenshot(path=os.path.join(ROOT, "screenshots", shot), full_page=True)
        print("saved", shot)
    browser.close()
