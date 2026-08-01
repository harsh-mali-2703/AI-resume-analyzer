import io
import csv

import streamlit as st

from job_matcher import build_role_text, calculate_role_matches, get_role_by_name
from resume_parser import extract_resume_text
from roadmap_generator import create_roadmap
from skill_extractor import extract_skills, group_skills
from text_cleaner import clean_resume_text


st.set_page_config(page_title="AI Resume Analyzer", page_icon="📄", layout="wide")


def load_data():
    # The project keeps its job roles and skills in CSV files so the data can be edited easily.
    with open("data/job_roles.csv", newline="", encoding="utf-8") as file:
        jobs = list(csv.DictReader(file))

    with open("data/skill_dictionary.csv", newline="", encoding="utf-8") as file:
        skills = list(csv.DictReader(file))

    return jobs, skills


def make_text_report(file_name, target_role, found_skills, missing_skills, top_roles, roadmap):
    # This plain-text report is generated from the same values shown on the dashboard.
    lines = [
        "AI Resume Analyzer Report",
        "",
        f"Resume file: {file_name}",
        f"Target role: {target_role}",
        "",
        "Skills found:",
        ", ".join(found_skills) if found_skills else "No matching skills found",
        "",
        "Missing skills:",
        ", ".join(missing_skills) if missing_skills else "No major missing skills",
        "",
        "Recommended roles:",
    ]

    for role in top_roles:
        lines.append(f"- {role['job_role']}: {role['score']}%")

    lines.extend(["", "Learning roadmap:"])
    for item in roadmap:
        lines.append(f"- {item}")

    lines.extend(
        [
            "",
            "Note: This is only an estimated score for learning guidance. It should not be used for final hiring decisions.",
        ]
    )
    return "\n".join(lines)


def main():
    st.title("AI Resume Analyzer and Job Recommendation System")
    st.caption("A simple NLP based mini project for checking resume skill match with job roles.")

    try:
        jobs_df, skills_df = load_data()
    except FileNotFoundError:
        st.error("Dataset files are missing. Please check the data folder.")
        return

    role_names = [job["job_role"] for job in jobs_df]

    with st.sidebar:
        # Sidebar inputs keep the main page focused on results after the resume is uploaded.
        st.header("Input")
        uploaded_file = st.file_uploader("Upload resume", type=["pdf", "docx"])
        target_role = st.selectbox("Choose target role", role_names)
        show_resume_text = st.checkbox("Show extracted text")

        st.info(
            "This tool checks only job related information like skills, projects and experience."
        )

    if uploaded_file is None:
        st.write("Upload a PDF or DOCX resume to start the analysis.")
        st.dataframe(
            [{"job_role": job["job_role"], "required_skills": job["required_skills"]} for job in jobs_df],
            use_container_width=True,
        )
        return

    try:
        resume_text = extract_resume_text(uploaded_file)
    except Exception as error:
        st.error(f"Could not read this file: {error}")
        return

    cleaned_text = clean_resume_text(resume_text)
    if len(cleaned_text) < 20:
        st.error(
            "No readable text was found in this resume. This usually happens when the PDF is scanned or image based. "
            "Please upload a DOCX resume, a text-based PDF, or convert the PDF with OCR first."
        )
        st.info("Tip: tick 'Show extracted text' after uploading another file to check what the app can read.")
        return

    found_skills = extract_skills(cleaned_text, skills_df)
    skill_groups = group_skills(found_skills, skills_df)
    role_matches = calculate_role_matches(cleaned_text, jobs_df)
    top_roles = role_matches[:3]

    # Compare the detected resume skills with the required skills of the selected role.
    selected_role = get_role_by_name(jobs_df, target_role)
    required_skills = [skill.strip() for skill in selected_role["required_skills"].split(",")]
    found_lower = {skill.lower() for skill in found_skills}
    missing_skills = [skill for skill in required_skills if skill.lower() not in found_lower]
    matched_required = [skill for skill in required_skills if skill.lower() in found_lower]
    roadmap = create_roadmap(missing_skills)

    role_text = build_role_text(selected_role)
    target_score = calculate_role_matches(cleaned_text, [selected_role])[0]["score"]

    col1, col2, col3 = st.columns(3)
    col1.metric("Target Match", f"{target_score}%")
    col2.metric("Skills Found", len(found_skills))
    col3.metric("Missing Skills", len(missing_skills))

    left, right = st.columns([1.1, 1])

    with left:
        st.subheader("Recommended Roles")
        chart_data = {role["job_role"]: role["score"] for role in top_roles}
        st.bar_chart(chart_data)
        st.dataframe(top_roles, use_container_width=True)

        st.subheader("Extracted Skills")
        if skill_groups:
            for category, skills in skill_groups.items():
                st.write(f"**{category.title()}**: {', '.join(skills)}")
        else:
            st.warning("No skills from the dictionary were detected.")

    with right:
        st.subheader("Target Role Skill Gap")
        st.write(f"**Role checked:** {target_role}")
        st.write(f"**Role keywords used:** {role_text}")
        st.write("**Matched skills:**")
        st.write(", ".join(matched_required) if matched_required else "No required skills matched.")
        st.write("**Missing skills:**")
        st.write(", ".join(missing_skills) if missing_skills else "Good match for required skills.")

        st.subheader("Learning Roadmap")
        for point in roadmap:
            st.write(f"- {point}")

    if show_resume_text:
        st.subheader("Extracted Resume Text")
        st.text_area("Text", resume_text, height=220)

    report = make_text_report(
        uploaded_file.name, target_role, found_skills, missing_skills, top_roles, roadmap
    )
    st.download_button(
        "Download analysis report",
        data=io.BytesIO(report.encode("utf-8")),
        file_name="resume_analysis_report.txt",
        mime="text/plain",
    )

    st.caption(
        "Match score is an estimate. Missing keywords do not always mean the student does not know the skill."
    )


if __name__ == "__main__":
    main()
