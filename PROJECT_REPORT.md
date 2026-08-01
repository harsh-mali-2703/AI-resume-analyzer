# AI Resume Analyzer and Job Recommendation System

## Objective

The aim of this project is to make a simple NLP based application that helps students check how well their resume matches different job roles. It gives a match score, shows missing skills and suggests a small learning roadmap.

## Modules

1. Resume upload for PDF and DOCX files.
2. Text extraction and cleaning.
3. Skill extraction using a manually prepared skill dictionary.
4. Job matching using TF-IDF and cosine similarity.
5. Skill gap analysis for the selected target role.
6. Streamlit dashboard and downloadable text report.

## Method Used

The resume text is converted to lowercase and cleaned with regular expressions. Skills are detected by matching words from `skill_dictionary.csv`. For recommendation, the resume text and job role descriptions are converted into TF-IDF vectors. Cosine similarity is used to calculate the matching score.

## Responsible AI Points

This project is only for learning and resume improvement guidance. It does not use personal details like gender, age, religion, photograph, nationality or marital status. The score is only an estimate and should not be used for final hiring or rejection.

## Limitations

Keyword matching can miss skills when the resume uses different wording. The dataset is small and manually created. The project can be improved later with Sentence Transformers, larger job datasets and better resume section detection.
