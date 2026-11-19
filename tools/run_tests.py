"""Runs the 5 sample test cases and saves the outputs to test_results.md."""
import json, os, sys, time
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))
from analyzer import analyze, read_resume, MODEL

S = os.path.join(os.path.dirname(__file__), "..", "samples")
CASES = [
    ("resume_python_dev.pdf", "jd_backend_python.txt", "strong fit"),
    ("resume_python_dev.pdf", "jd_frontend_react.txt", "partial fit"),
    ("resume_data_analyst.pdf", "jd_data_analyst.txt", "strong fit"),
    ("resume_data_analyst.pdf", "jd_ml_engineer.txt", "partial fit"),
    ("resume_mechanical.pdf", "jd_backend_python.txt", "weak fit"),
]
out = [f"# Test results (model: {MODEL})\n"]
for resume, jd, expected in CASES:
    t = time.time()
    r = analyze(read_resume(open(os.path.join(S, resume), "rb")), open(os.path.join(S, jd)).read())
    secs = time.time() - t
    print(f"{resume:26} vs {jd:24} expected {expected:11} -> score {r['match_score']:3}  ({secs:.1f}s)")
    out.append(f"## {resume} vs {jd} (expected: {expected})\n\nTime: {secs:.1f} s\n\n```json\n{json.dumps(r, indent=2)}\n```\n")
open(os.path.join(S, "..", "test_results.md"), "w", encoding="utf-8").write("\n".join(out))
