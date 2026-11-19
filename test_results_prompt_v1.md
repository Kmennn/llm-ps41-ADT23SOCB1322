# Test results (model: qwen2.5-14b-instruct)

## resume_python_dev.pdf vs jd_backend_python.txt (expected: strong fit)

Time: 5.3 s

```json
{
  "match_score": 75,
  "matched_skills": [
    "Python",
    "Django",
    "REST APIs",
    "PostgreSQL",
    "Git",
    "Docker"
  ],
  "missing_skills": [
    "FastAPI",
    "AWS",
    "Redis",
    "unit testing with pytest",
    "CI/CD"
  ],
  "tips": [
    "Add experience with FastAPI if relevant.",
    "Include any AWS experience or certifications.",
    "Mention any unit testing with pytest and CI/CD knowledge."
  ],
  "summary": "Aarav Sharma has a strong foundation in Python, Django, REST APIs, PostgreSQL, Git, and Docker, aligning well with the job requirements. Additional skills in FastAPI, AWS, Redis, and CI/CD would enhance the fit."
}
```

## resume_python_dev.pdf vs jd_frontend_react.txt (expected: partial fit)

Time: 3.6 s

```json
{
  "match_score": 30,
  "matched_skills": [
    "HTML",
    "CSS",
    "REST API integration",
    "Git"
  ],
  "missing_skills": [
    "JavaScript",
    "React",
    "TypeScript",
    "Next.js",
    "Tailwind",
    "testing with Jest"
  ],
  "tips": [
    "Add JavaScript and React skills to your resume.",
    "Include any experience or projects using TypeScript and Next.js.",
    "Mention any testing experience, especially with Jest."
  ],
  "summary": "The resume shows limited overlap with the frontend developer role, focusing more on backend technologies."
}
```

## resume_data_analyst.pdf vs jd_data_analyst.txt (expected: strong fit)

Time: 4.0 s

```json
{
  "match_score": 85,
  "matched_skills": [
    "SQL",
    "Excel",
    "Power BI",
    "Python (pandas)",
    "data cleaning",
    "statistics"
  ],
  "missing_skills": [
    "Tableau",
    "A/B testing",
    "communication skills"
  ],
  "tips": [
    "Include Tableau experience or training if available",
    "Add projects or experience related to A/B testing",
    "Highlight communication skills in the resume"
  ],
  "summary": "Priya has a strong match with the job requirements, showing proficiency in SQL, Excel, Power BI, Python, and data cleaning. Additional skills like Tableau and A/B testing would further enhance her fit."
}
```

## resume_data_analyst.pdf vs jd_ml_engineer.txt (expected: partial fit)

Time: 4.7 s

```json
{
  "match_score": 45,
  "matched_skills": [
    "Python",
    "SQL",
    "statistics"
  ],
  "missing_skills": [
    "scikit-learn",
    "TensorFlow or PyTorch",
    "model deployment",
    "MLOps",
    "Docker",
    "cloud (AWS/GCP)"
  ],
  "tips": [
    "Add experience or projects related to machine learning frameworks like scikit-learn and TensorFlow/PyTorch.",
    "Include any work on model deployment or MLOps.",
    "Mention any experience with Docker and cloud platforms like AWS or GCP."
  ],
  "summary": "The candidate has a partial fit for the role, showing basic Python and data analysis skills but lacking in machine learning frameworks and deployment experience."
}
```

## resume_mechanical.pdf vs jd_backend_python.txt (expected: weak fit)

Time: 4.0 s

```json
{
  "match_score": 0,
  "matched_skills": [],
  "missing_skills": [
    "Python",
    "Django",
    "FastAPI",
    "REST APIs",
    "PostgreSQL",
    "Git",
    "Docker",
    "AWS",
    "Redis",
    "unit testing with pytest",
    "CI/CD"
  ],
  "tips": [
    "Add Python and Django to your skills section.",
    "Include any experience or projects related to backend development.",
    "Mention any knowledge of REST APIs, PostgreSQL, Git, Docker, AWS, Redis, pytest, and CI/CD."
  ],
  "summary": "The resume does not match the job description as it focuses on mechanical engineering skills and lacks any backend development experience or skills."
}
```
