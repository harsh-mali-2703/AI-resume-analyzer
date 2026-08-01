import re


def _skill_pattern(skill):
    escaped = re.escape(skill.lower())
    # Custom boundaries stop partial matches, for example "sql" inside another word.
    return r"(?<![a-z0-9+#.])" + escaped + r"(?![a-z0-9+#.])"


def extract_skills(cleaned_text, skills_df):
    found = []

    # Each skill from the dictionary is searched against the cleaned resume text.
    for row in skills_df:
        skill = str(row["skill"]).strip()
        if not skill:
            continue

        if re.search(_skill_pattern(skill), cleaned_text):
            found.append(skill)

    return sorted(set(found), key=str.lower)


def group_skills(found_skills, skills_df):
    groups = {}
    # Build a quick lookup so detected skills can be displayed under their categories.
    lookup = {
        str(row["skill"]).lower(): str(row["category"])
        for row in skills_df
    }

    for skill in found_skills:
        category = lookup.get(skill.lower(), "other")
        groups.setdefault(category, []).append(skill)

    return groups
