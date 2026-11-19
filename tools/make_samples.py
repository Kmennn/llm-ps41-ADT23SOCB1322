"""Creates the sample resumes (PDF) and job descriptions used for testing."""
import os
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

HERE = os.path.join(os.path.dirname(__file__), "..", "samples")
RESUMES = {
"resume_python_dev.pdf": """Aarav Sharma - Python Developer
Email: aarav.sample@example.com | Pune
SKILLS: Python, Django, REST APIs, PostgreSQL, Git, Docker, Linux, HTML, CSS
EXPERIENCE: Intern, Web Team, ABC Tech (6 months) - built Django REST APIs for an
inventory app, wrote SQL queries in PostgreSQL, deployed with Docker.
PROJECTS: Library management system (Django, PostgreSQL); Expense tracker (Flask).
EDUCATION: B.Tech Computer Engineering, 2026, CGPA 8.1""",
"resume_data_analyst.pdf": """Priya Kulkarni - Data Analyst
Email: priya.sample@example.com | Mumbai
SKILLS: Excel, SQL, Power BI, Python (pandas, matplotlib), statistics
EXPERIENCE: Data intern, Retail Co (4 months) - cleaned sales data in pandas,
built Power BI dashboards for monthly sales, wrote SQL reports.
PROJECTS: Sales dashboard in Power BI; Customer churn analysis in Python.
EDUCATION: B.Sc Statistics, 2026""",
"resume_mechanical.pdf": """Rohan Patil - Mechanical Engineer
Email: rohan.sample@example.com | Nashik
SKILLS: AutoCAD, SolidWorks, CATIA, GD&T, manufacturing processes
EXPERIENCE: Trainee, Auto Parts Ltd (6 months) - designed jigs in SolidWorks.
PROJECTS: Design of a solar dryer; FEA of a bracket in ANSYS.
EDUCATION: B.E. Mechanical Engineering, 2026""",
}
JDS = {
"jd_backend_python.txt": "Backend Developer (Fresher). Required: Python, Django or FastAPI, REST APIs, PostgreSQL, Git, Docker. Good to have: AWS, Redis, unit testing with pytest, CI/CD.",
"jd_ml_engineer.txt": "Machine Learning Engineer. Required: Python, scikit-learn, TensorFlow or PyTorch, model deployment, SQL, statistics. Good to have: MLOps, Docker, cloud (AWS/GCP).",
"jd_data_analyst.txt": "Data Analyst. Required: SQL, Excel, Power BI or Tableau, Python (pandas), data cleaning, communication skills. Good to have: statistics, A/B testing.",
"jd_frontend_react.txt": "Frontend Developer. Required: JavaScript, React, HTML, CSS, TypeScript, REST API integration, Git. Good to have: Next.js, Tailwind, testing with Jest.",
"jd_cad_designer.txt": "CAD Design Engineer. Required: SolidWorks, AutoCAD, GD&T, drawing standards, sheet metal design. Good to have: ANSYS, CATIA, PLM tools.",
}

for name, text in RESUMES.items():
    c = canvas.Canvas(os.path.join(HERE, name), pagesize=A4)
    y = 800
    for line in text.splitlines():
        c.drawString(50, y, line)
        y -= 18
    c.save()
for name, text in JDS.items():
    open(os.path.join(HERE, name), "w").write(text)
print("samples written")
