import re
from collections import Counter
from sklearn.feature_extraction.text import TfidfVectorizer


COMMON_SKILLS = [
    "python", "java", "c", "c++", "javascript", "typescript",
    "html", "css", "react", "node.js", "express", "mongodb",
    "mysql", "sql", "git", "github", "docker", "jenkins",
    "aws", "azure", "machine learning", "deep learning",
    "artificial intelligence", "data science", "pandas",
    "numpy", "matplotlib", "scikit-learn", "pytorch",
    "tensorflow", "streamlit", "flask", "django",
    "rest api", "fastapi", "linux", "cybersecurity"
]


def clean_text(text):
    text = text.lower()
    text = re.sub(r"[^a-zA-Z0-9+#.\s]", " ", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_skills(text):
    text_lower = text.lower()

    found = []

    for skill in COMMON_SKILLS:
        if skill.lower() in text_lower:
            found.append(skill)

    return sorted(set(found))


def extract_email(text):
    pattern = r"[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Za-z]{2,}"
    match = re.search(pattern, text)

    return match.group(0) if match else "Not found"


def extract_phone(text):
    pattern = r"(\+91[\s-]?)?[6-9]\d{9}"
    match = re.search(pattern, text)

    return match.group(0) if match else "Not found"


def calculate_keyword_match(resume_text, job_description):
    resume_words = set(clean_text(resume_text).split())
    job_words = set(clean_text(job_description).split())

    important_words = {
        word for word in job_words
        if len(word) > 2
    }

    if not important_words:
        return 0, []

    matched = resume_words.intersection(important_words)
    missing = important_words - resume_words

    score = (len(matched) / len(important_words)) * 100

    return round(score, 2), sorted(missing)


def calculate_ats_score(
    resume_text,
    job_description,
    skills,
    keyword_score
):
    score = 0

    # Keyword score - 50%
    score += keyword_score * 0.50

    # Skills - 20%
    if len(skills) >= 10:
        skill_score = 100
    else:
        skill_score = len(skills) * 10

    score += skill_score * 0.20

    # Resume sections - 20%
    sections = [
        "education",
        "experience",
        "skills",
        "projects",
        "certifications"
    ]

    resume_lower = resume_text.lower()

    section_count = sum(
        1 for section in sections
        if section in resume_lower
    )

    section_score = (section_count / len(sections)) * 100
    score += section_score * 0.20

    # Contact information - 10%
    email = extract_email(resume_text)
    phone = extract_phone(resume_text)

    contact_score = 100 if (
        email != "Not found" and phone != "Not found"
    ) else 50

    score += contact_score * 0.10

    return round(min(score, 100), 2)


def generate_suggestions(
    resume_text,
    missing_keywords,
    skills
):
    suggestions = []

    text = resume_text.lower()

    if "summary" not in text and "objective" not in text:
        suggestions.append(
            "Add a professional summary or career objective."
        )

    if "experience" not in text:
        suggestions.append(
            "Add an Experience section if you have internship or work experience."
        )

    if "projects" not in text:
        suggestions.append(
            "Add a Projects section with technologies and measurable results."
        )

    if "certification" not in text:
        suggestions.append(
            "Add relevant certifications to strengthen your resume."
        )

    if len(skills) < 5:
        suggestions.append(
            "Add more relevant technical skills that match the target job."
        )

    if missing_keywords:
        suggestions.append(
            "Add relevant missing keywords from the job description naturally."
        )

    if not suggestions:
        suggestions.append(
            "Your resume structure looks good. Continue improving measurable achievements."
        )

    return suggestions


def analyze_resume(resume_text, job_description):
    skills = extract_skills(resume_text)

    keyword_score, missing_keywords = calculate_keyword_match(
        resume_text,
        job_description
    )

    ats_score = calculate_ats_score(
        resume_text,
        job_description,
        skills,
        keyword_score
    )

    suggestions = generate_suggestions(
        resume_text,
        missing_keywords,
        skills
    )

    return {
        "ats_score": ats_score,
        "keyword_score": keyword_score,
        "skills": skills,
        "missing_keywords": missing_keywords[:30],
        "email": extract_email(resume_text),
        "phone": extract_phone(resume_text),
        "suggestions": suggestions
    }