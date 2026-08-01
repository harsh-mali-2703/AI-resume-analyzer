import re


def clean_resume_text(text):
    text = text.lower()

    # Keep a few technical symbols because skills like C++, C# and .NET need them.
    text = re.sub(r"[^a-z0-9+#.\s-]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()
