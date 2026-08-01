# AI Resume Analyzer and Job Recommendation System

This is a student mini project made using Python and Streamlit. The app reads a PDF or DOCX resume, extracts skills, compares the resume with job roles and gives a simple learning roadmap.

## Features

- Upload PDF or DOCX resume
- Extract and clean resume text
- Detect skills from a small skill dictionary
- Compare resume with job roles using TF-IDF and cosine similarity
- Show top 3 recommended roles
- Show missing skills for selected role
- Generate a basic weekly roadmap
- Download analysis report as text file

## Folder Structure

```text
ai_resume_analyzer/
|-- app.py
|-- resume_parser.py
|-- text_cleaner.py
|-- skill_extractor.py
|-- job_matcher.py
|-- roadmap_generator.py
|-- requirements.txt
|-- README.md
|-- PROJECT_REPORT.md
|-- architecture.md
|-- data/
|   |-- job_roles.csv
|   |-- skill_dictionary.csv
|   |-- test_cases.csv
|   |-- sample_resumes/
|-- reports/
|-- tests/
```

## Installation

```bash
pip install -r requirements.txt
```

## Run Project

```bash
streamlit run app.py
```

## How It Works

1. User uploads a resume.
2. Text is extracted from the resume.
3. Text is cleaned and normalized.
4. Skills are matched with `skill_dictionary.csv`.
5. Resume text is compared with job role descriptions.
6. App shows match score, top roles, missing skills and roadmap.

## Future Improvements

- Add custom job description upload
- Add PDF report generation
- Improve skill extraction using spaCy
- Use Sentence Transformers for better semantic matching
- Add more roles and skills in dataset

## Note

This project is for educational guidance only. Match score is an estimated value and should not be used for automatic hiring decisions.
