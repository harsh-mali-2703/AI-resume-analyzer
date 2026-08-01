from skill_extractor import extract_skills
from text_cleaner import clean_resume_text


def test_skill_extraction_finds_keywords():
    skills = [
        {"skill": "Python", "category": "programming"},
        {"skill": "SQL", "category": "database"},
        {"skill": "Docker", "category": "tools"},
    ]
    text = clean_resume_text("I know Python, SQL and basic dashboards.")
    found = extract_skills(text, skills)
    assert "Python" in found
    assert "SQL" in found
    assert "Docker" not in found
