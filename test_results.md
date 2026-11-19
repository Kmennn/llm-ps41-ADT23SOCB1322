# Test results (model: qwen2.5-14b-instruct)

## resume_python_dev.pdf vs jd_backend_python.txt (expected: strong fit)

Time: 6.2 s

```json
{
  "match_score": 85,
  "matched_skills": [
    "Python",
    "Django",
    "REST APIs",
    "PostgreSQL",
    "Git",
    "Docker"
  ],
  "missing_skills": [
    "AWS",
    "Redis",
    "unit testing with pytest",
    "CI/CD (good to have)"
  ],
  "tips": [
    "Add experience with FastAPI to match all required skills.",
    "Include any knowledge or experience with AWS and Redis.",
    "Mention any unit testing experience with pytest and CI/CD practices."
  ],
  "summary": "Aarav Sharma is a strong fit for the Backend Developer role with all required skills except FastAPI. Adding experience with FastAPI and good-to-have skills would improve the fit."
}
```

## resume_python_dev.pdf vs jd_frontend_react.txt (expected: partial fit)

Time: 3.7 s

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
    "testing with Jest (good to have)"
  ],
  "tips": [
    "Add JavaScript and React to your skills section.",
    "Include experience with TypeScript and Next.js if applicable.",
    "Highlight any testing experience with Jest or similar tools."
  ],
  "summary": "The resume shows limited frontend development skills, primarily focusing on backend technologies. Significant gaps in required frontend skills."
}
```

## resume_data_analyst.pdf vs jd_data_analyst.txt (expected: strong fit)

Time: 4.5 s

```json
{
  "match_score": 85,
  "matched_skills": [
    "SQL",
    "Excel",
    "Power BI",
    "Python (pandas)",
    "data cleaning"
  ],
  "missing_skills": [
    "statistics",
    "A/B testing (good to have)"
  ],
  "tips": [
    "Include Tableau in your skills if you have any experience with it.",
    "Highlight your statistics knowledge and any A/B testing experience.",
    "Emphasize your communication skills in your resume summary and experience section."
  ],
  "summary": "Priya Kulkarni is a strong fit for the Data Analyst role with all required skills covered, except for Tableau. Adding statistics and A/B testing experience would further enhance her profile."
}
```

## resume_data_analyst.pdf vs jd_ml_engineer.txt (expected: partial fit)

Time: 4.5 s

```json
{
  "match_score": 65,
  "matched_skills": [
    "Python",
    "statistics",
    "SQL"
  ],
  "missing_skills": [
    "scikit-learn",
    "TensorFlow or PyTorch",
    "model deployment",
    "MLOps",
    "Docker",
    "cloud (AWS/GCP) (good to have)"
  ],
  "tips": [
    "Add experience with scikit-learn and TensorFlow or PyTorch to your resume.",
    "Include any experience with model deployment.",
    "Mention any familiarity with MLOps, Docker, and cloud services like AWS or GCP."
  ],
  "summary": "The candidate has a partial fit for the Machine Learning Engineer role with experience in Python, SQL, and statistics, but lacks the required skills in machine learning frameworks and model deployment."
}
```

## resume_mechanical.pdf vs jd_backend_python.txt (expected: weak fit)

Time: 4.1 s

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
    "CI/CD (good to have)"
  ],
  "tips": [
    "Add Python and Django/FastAPI experience to your resume.",
    "Include any experience with REST APIs, PostgreSQL, Git, and Docker.",
    "Mention any knowledge of AWS, Redis, and CI/CD tools like pytest."
  ],
  "summary": "The resume does not match the job description as it lacks all the required backend development skills and experience."
}
```
