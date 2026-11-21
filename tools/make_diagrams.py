"""Draws the block diagram and flowchart used in the report and PPT.
Output: docs/block_diagram.png, docs/flowchart.png"""
import os
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch

OUT = os.path.join(os.path.dirname(__file__), "..", "docs")
BLUE, GREEN, ORANGE, PURPLE, GREY = "#dbeafe", "#dcfce7", "#ffedd5", "#ede9fe", "#f1f5f9"


def box(ax, x, y, w, h, text, color, shape="round"):
    style = "round,pad=0.02,rounding_size=0.15" if shape == "round" else "square,pad=0.02"
    ax.add_patch(FancyBboxPatch((x - w / 2, y - h / 2), w, h, boxstyle=style,
                                fc=color, ec="#334155", lw=1.4))
    ax.text(x, y, text, ha="center", va="center", fontsize=10, wrap=True)


def diamond(ax, x, y, w, h, text):
    ax.add_patch(plt.Polygon([(x, y + h / 2), (x + w / 2, y), (x, y - h / 2), (x - w / 2, y)],
                             fc="#fef9c3", ec="#334155", lw=1.4))
    ax.text(x, y, text, ha="center", va="center", fontsize=9.5)


def arrow(ax, x1, y1, x2, y2, label=None):
    ax.annotate("", xy=(x2, y2), xytext=(x1, y1),
                arrowprops=dict(arrowstyle="-|>", color="#334155", lw=1.4))
    if label:
        ax.text((x1 + x2) / 2 + 0.1, (y1 + y2) / 2 + 0.1, label, fontsize=9, color="#b91c1c")


def block_diagram():
    fig, ax = plt.subplots(figsize=(11, 5.2))
    ax.set_xlim(0, 11); ax.set_ylim(0, 5.2); ax.axis("off")
    ax.text(5.5, 4.95, "Block diagram: Resume Analyzer", ha="center", fontsize=14, weight="bold")
    box(ax, 1.2, 3.6, 1.9, 0.9, "User\n(student)", GREY)
    box(ax, 3.7, 3.6, 2.3, 1.05, "Web page (browser)\nindex.html\npdf.js reads the PDF", BLUE)
    box(ax, 6.6, 3.6, 2.4, 1.05, "Vercel function\napp.py (Flask)\nanalyzer.py: prompt", GREEN)
    box(ax, 9.5, 3.6, 2.4, 1.05, "Secure tunnel\nCloudflare HTTPS +\nsecret API key", GREY)
    box(ax, 9.5, 1.4, 2.4, 1.05, "LLM server, lab node 04\nQwen2.5-14B (llama.cpp)\nNVIDIA H200 GPU slice", PURPLE)
    box(ax, 6.6, 1.4, 2.4, 1.05, "Validator\nJSON parse, clamp 0-100,\nretry, 'A or B' fix", ORANGE)
    box(ax, 3.7, 1.4, 2.3, 1.05, "Result view\nscore ring, skills,\n3 tips, summary", BLUE)
    arrow(ax, 2.15, 3.6, 2.55, 3.6)
    arrow(ax, 4.85, 3.6, 5.4, 3.6)
    arrow(ax, 7.8, 3.6, 8.3, 3.6)
    arrow(ax, 9.5, 3.07, 9.5, 1.93, "")
    arrow(ax, 8.3, 1.4, 7.8, 1.4)
    arrow(ax, 5.4, 1.4, 4.85, 1.4)
    ax.text(10.9, 2.5, "OpenAI-compatible\nAPI over HTTPS", ha="center", fontsize=8.5, style="italic")
    ax.text(3.7, 4.35, "the PDF file never leaves the user's computer", ha="center", fontsize=8.5, style="italic", color="#475569")
    fig.savefig(os.path.join(OUT, "block_diagram.png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


def flowchart():
    fig, ax = plt.subplots(figsize=(7.5, 11))
    ax.set_xlim(0, 7.5); ax.set_ylim(0, 11); ax.axis("off")
    ax.text(3.75, 10.75, "Flowchart: one analysis", ha="center", fontsize=14, weight="bold")
    x = 3.2
    steps = [
        (10.1, "Start", GREY, "round"),
        (9.2, "Upload resume (PDF) and\npaste job description", BLUE, "sq"),
    ]
    for y, t, c, s in steps:
        box(ax, x, y, 3.2, 0.65, t, c, "round" if s == "round" else "sq")
    arrow(ax, x, 9.77, x, 9.53)
    diamond(ax, x, 8.15, 3.0, 1.0, "Both inputs\ngiven?")
    arrow(ax, x, 8.87, x, 8.65)
    box(ax, 6.3, 8.15, 1.9, 0.65, "Show warning", "#fee2e2", "sq")
    arrow(ax, 4.7, 8.15, 5.35, 8.15, "No")
    box(ax, x, 7.0, 3.2, 0.65, "Browser reads PDF text\n(pdf.js)", GREEN, "sq")
    arrow(ax, x, 7.65, x, 7.33, "Yes")
    diamond(ax, x, 5.85, 3.0, 1.0, "Text found?")
    arrow(ax, x, 6.67, x, 6.35)
    box(ax, 6.3, 5.85, 1.9, 0.75, "Error: scanned\nPDF, no text", "#fee2e2", "sq")
    arrow(ax, 4.7, 5.85, 5.35, 5.85, "No")
    box(ax, x, 4.7, 3.2, 0.65, "Send text to Vercel API;\ncall LLM on lab node 04", PURPLE, "sq")
    arrow(ax, x, 5.35, x, 5.03, "Yes")
    diamond(ax, x, 3.55, 3.0, 1.0, "Valid JSON?")
    arrow(ax, x, 4.37, x, 4.05)
    box(ax, 6.3, 3.55, 1.9, 0.75, "Ask again:\n'JSON only'\n(1 retry)", ORANGE, "sq")
    arrow(ax, 4.7, 3.55, 5.35, 3.55, "No")
    arrow(ax, 6.3, 3.95, 4.8, 4.6)
    box(ax, x, 2.4, 3.2, 0.75, "Clean: clamp score 0-100,\n3 tips, fix 'A or B' skills", ORANGE, "sq")
    arrow(ax, x, 3.05, x, 2.78, "Yes")
    box(ax, x, 1.3, 3.2, 0.65, "Show score bar, skills, tips", BLUE, "sq")
    arrow(ax, x, 2.02, x, 1.63)
    box(ax, x, 0.4, 2.0, 0.55, "End", GREY)
    arrow(ax, x, 0.97, x, 0.68)
    fig.savefig(os.path.join(OUT, "flowchart.png"), dpi=160, bbox_inches="tight")
    plt.close(fig)


if __name__ == "__main__":
    block_diagram()
    flowchart()
    print("diagrams written to docs/")
