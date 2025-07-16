# utils/github_analyzer.py
"""
GitHub analysis utilities for SkillGuardian.
"""

from typing import Dict
import requests
import re

GITHUB_API = "https://api.github.com"


def fetch_github_profile_stats(github_url: str) -> Dict:
    """
    Fetches GitHub profile statistics and project topics using the GitHub API.
    Args:
        github_url: The user's GitHub profile URL.
    Returns:
        Dictionary with username, repo_count, languages, and topics.
    """
    # Extract username from URL
    match = re.match(r"https?://github.com/([A-Za-z0-9-]+)", github_url.strip())
    if not match:
        return {"error": "Invalid GitHub URL."}
    username = match.group(1)
    headers = {"Accept": "application/vnd.github.v3+json"}
    user_url = f"{GITHUB_API}/users/{username}"
    repos_url = f"{GITHUB_API}/users/{username}/repos?per_page=100"
    try:
        user_resp = requests.get(user_url, headers=headers)
        if user_resp.status_code != 200:
            return {"error": f"GitHub user not found: {username}"}
        user_data = user_resp.json()
        repos_resp = requests.get(repos_url, headers=headers)
        repos = repos_resp.json() if repos_resp.status_code == 200 else []
        repo_count = user_data.get("public_repos", 0)
        languages = set()
        topics = set()
        for repo in repos:
            lang = repo.get("language")
            if lang:
                languages.add(lang)
            repo_topics_url = repo.get("url", "") + "/topics"
            topics_resp = requests.get(repo_topics_url, headers={**headers, "Accept": "application/vnd.github.mercy-preview+json"})
            if topics_resp.status_code == 200:
                repo_topics = topics_resp.json().get("names", [])
                topics.update(repo_topics)
        return {
            "username": username,
            "repo_count": repo_count,
            "languages": list(languages),
            "topics": list(topics)
        }
    except Exception as e:
        return {"error": str(e)} 