# SkillGuardian – Real-Time Skill Gap Notifier + Job Match AI

## Overview
SkillGuardian is an AI-powered web application that analyzes a user’s resume, GitHub profile, and career goal to generate a personalized skill gap report. It helps students and early-career professionals understand what skills they're missing to reach their target job roles and suggests learning paths and project ideas to bridge the gap.

## Features
- Upload resume (PDF)
- Analyze GitHub profile
- Enter career goal
- AI-powered skill gap report (OpenAI GPT-4)
- Dashboard with extracted skills, GitHub stats, and recommendations
- Data storage with Firebase

## Tech Stack
- Frontend: Streamlit (Python)
- Backend: Python
- Resume Parsing: PyMuPDF, PyPDF2
- GitHub Data: GitHub API
- AI/NLP: OpenAI API (GPT-4)
- Database: Firebase (Firestore)

## Setup Instructions
1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Set up your `.env` file (see `.env.example`) with your OpenAI and Firebase credentials.
4. Run the app:
   ```bash
   streamlit run app.py
   ```

## Deployment (Streamlit Cloud)

1. **Push your code to GitHub.**
2. **Go to [Streamlit Cloud](https://share.streamlit.io/)** and sign in with GitHub.
3. **Create a new app:**
   - Select your repository and `app.py` as the entry point.
4. **Set environment variables:**
   - In the app settings, add:
     - `OPENAI_API_KEY` (your OpenAI key)
     - `FIREBASE_CREDENTIALS` (path to your Firebase credentials JSON file)
5. **Upload your Firebase credentials file:**
   - In Streamlit Cloud, go to the app’s “Files” tab and upload your `firebase-credentials.json` file.
   - Set `FIREBASE_CREDENTIALS` to `/mount/src/firebase-credentials.json` or the correct path.
6. **Deploy!**

## Usage
1. Upload your resume (PDF)
2. Enter your GitHub profile URL
3. Enter your target career goal (e.g., "Backend Developer at Amazon")
4. View your personalized skill gap report and recommendations

## License
MIT 