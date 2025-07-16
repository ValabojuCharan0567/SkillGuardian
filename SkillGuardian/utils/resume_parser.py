# utils/resume_parser.py
"""
Resume parsing utilities for SkillGuardian.
"""

from typing import List, Tuple
import fitz  # PyMuPDF
import re

# A basic set of common tech skills for demo purposes
COMMON_SKILLS = [
    'python', 'java', 'c++', 'c#', 'javascript', 'typescript', 'react', 'angular', 'vue', 'node',
    'django', 'flask', 'spring', 'express', 'html', 'css', 'sql', 'mongodb', 'firebase', 'aws',
    'azure', 'gcp', 'docker', 'kubernetes', 'git', 'linux', 'tensorflow', 'pytorch', 'nlp', 'ml',
    'machine learning', 'deep learning', 'data science', 'rest', 'graphql', 'api', 'oop', 'agile',
    'scrum', 'jira', 'ci/cd', 'unit testing', 'selenium', 'pandas', 'numpy', 'matplotlib', 'scikit-learn'
]

def extract_text_and_skills_from_pdf(pdf_file) -> Tuple[str, List[str]]:
    """
    Extracts raw text and a list of detected skills from a PDF resume.
    Args:
        pdf_file: A file-like object containing the PDF.
    Returns:
        Tuple of (raw_text, skills_list)
    """
    # Extract text using PyMuPDF
    text = ""
    try:
        with fitz.open(stream=pdf_file.read(), filetype="pdf") as doc:
            for page in doc:
                text += page.get_text()
    except Exception as e:
        text = ""
    # Lowercase for skill matching
    text_lower = text.lower()
    # Extract skills by matching against COMMON_SKILLS
    found_skills = []
    for skill in COMMON_SKILLS:
        # Use word boundaries for accurate matching
        if re.search(r'\b' + re.escape(skill) + r'\b', text_lower):
            found_skills.append(skill)
    return text, found_skills 