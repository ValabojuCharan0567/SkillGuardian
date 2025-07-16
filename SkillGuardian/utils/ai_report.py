# utils/ai_report.py
"""
AI report generation utilities for SkillGuardian.
"""

from typing import Dict
import openai
import os

openai.api_key = os.getenv("OPENAI_API_KEY")

PROMPT_TEMPLATE = """
You are SkillGuardian, an expert career coach AI. Analyze the following user data and generate a professional skill gap report:

Resume/GitHub Skills:
{skills}

GitHub Stats:
- Languages: {languages}
- Topics: {topics}
- Repo Count: {repo_count}

Career Goal:
{career_goal}

Instructions:
1. List missing skills required for the target role.
2. Suggest 3-5 high-quality online resources (courses, docs, etc.) to learn these skills.
3. Recommend 2-3 project ideas to build portfolio strength for this goal.
4. Estimate a realistic timeline (in months) to bridge the gap.
5. Be concise, actionable, and use markdown formatting.
"""

def generate_skill_gap_report(skills: list, github_stats: dict, career_goal: str) -> Dict:
    """
    Calls OpenAI API to generate a personalized skill gap report.
    Args:
        skills: List of extracted skills from resume and GitHub.
        github_stats: Dictionary of GitHub profile stats.
        career_goal: Target job role entered by user.
    Returns:
        Dictionary with missing skills, resources, project ideas, and time estimates.
    """
    prompt = PROMPT_TEMPLATE.format(
        skills=", ".join(skills),
        languages=", ".join(github_stats.get("languages", [])),
        topics=", ".join(github_stats.get("topics", [])),
        repo_count=github_stats.get("repo_count", 0),
        career_goal=career_goal
    )
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "You are a helpful AI career coach."},
                      {"role": "user", "content": prompt}],
            max_tokens=800,
            temperature=0.7
        )
        report_md = response.choices[0].message.content.strip()
        return {"report_markdown": report_md}
    except Exception as e:
        return {"error": str(e)} 