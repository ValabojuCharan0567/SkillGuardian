import streamlit as st
from utils.resume_parser import extract_text_and_skills_from_pdf
from utils.github_analyzer import fetch_github_profile_stats
from utils.ai_report import generate_skill_gap_report
from utils.firebase_store import save_user_report, get_user_reports
import uuid
from datetime import datetime

st.set_page_config(page_title="SkillGuardian – Real-Time Skill Gap Notifier + Job Match AI", page_icon="🛡️", layout="centered")
st.markdown("""
<style>
    .main {background-color: #f8fafc;}
    .stTextInput>div>div>input {font-size: 1.1rem;}
    .stButton>button {font-size: 1.1rem;}
    .stMarkdown {font-size: 1.05rem;}
    h1, h2, h3, h4, h5, h6 {color: #1a202c !important; font-family: 'Segoe UI', Arial, sans-serif;}
    .stAlert {font-size: 1.05rem;}
</style>
""", unsafe_allow_html=True)

# Sidebar branding
with st.sidebar:
    st.markdown("""
    <div style='text-align:center;'>
        <span style='font-size:2.5rem;'>🛡️</span><br/>
        <span style='font-size:1.5rem;font-weight:bold;'>SkillGuardian</span><br/>
        <span style='font-size:1rem;color:#2563eb;'>Real-Time Skill Gap Notifier + Job Match AI</span>
    </div>
    <hr style='margin:0.5rem 0;' />
    """, unsafe_allow_html=True)
    st.markdown("""
    <div style='text-align:center;margin-top:1.5em;'>
        <a href='mailto:charanvalaboju@gmail.com?subject=SkillGuardian%20Feedback' target='_blank' style='text-decoration:none;'>
            <span style='font-size:1.1rem;'>💬 Give Feedback or Report a Bug</span>
        </a>
    </div>
    """, unsafe_allow_html=True)

# Sidebar navigation
page = st.sidebar.selectbox("Navigate", ["Skill Gap Analyzer", "Dashboard"], help="Choose a page to analyze your skills or view your reports.")

# Generate or get session user_id
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(uuid.uuid4())
user_id = st.session_state['user_id']

def format_timestamp(ts):
    if not ts:
        return "Unknown time"
    if isinstance(ts, str):
        try:
            ts = datetime.fromisoformat(ts)
        except Exception:
            return ts
    elif hasattr(ts, 'isoformat'):
        ts = ts.replace(tzinfo=None)
    return ts.strftime('%Y-%m-%d %H:%M:%S')

PRIMARY_COLOR = "#1a202c"  # High contrast dark blue/black
ACCENT_COLOR = "#fbbf24"    # High contrast gold

if page == "Skill Gap Analyzer":
    st.markdown(f"<h4 style='color:{PRIMARY_COLOR};font-size:1.5rem;'>Welcome to SkillGuardian!</h4>", unsafe_allow_html=True)
    st.info("Upload your resume, enter your GitHub profile, and specify your career goal to get a personalized skill gap report.")
    st.divider()

    # Resume Upload
    st.header("1. Upload Your Resume (PDF)", help="Step 1: Upload your resume in PDF format.")
    resume_file = st.file_uploader(
        "Choose your resume (PDF only)", type=["pdf"],
        help="Only PDF files are supported. We'll extract your skills and experience using AI."
    )
    st.divider()

    # GitHub URL Input
    st.header("2. Enter Your GitHub Profile URL", help="Step 2: Paste your public GitHub profile URL.")
    github_url = st.text_input(
        "GitHub Profile URL",
        placeholder="https://github.com/yourusername",
        help="Paste your public GitHub profile URL. We'll analyze your languages, repos, and topics.",
        key="github_url_input"
    )
    st.divider()

    # Career Goal Input
    st.header("3. Enter Your Target Career Goal", help="Step 3: Describe your dream job or target role.")
    career_goal = st.text_input(
        "Career Goal",
        placeholder="e.g., Backend Developer at Amazon",
        help="Describe your dream job or target role.",
        key="career_goal_input"
    )
    st.divider()

    # Submit Button
    if st.button("Analyze My Skill Gap", type="primary", help="Click to analyze your skills and get a personalized report."):
        # Resume Parsing
        skills = []
        text = ""
        if resume_file is not None:
            with st.spinner("Parsing your resume..."):
                text, skills = extract_text_and_skills_from_pdf(resume_file)
            st.success("Resume parsed successfully! Skills extracted below.")
            st.subheader("Extracted Resume Text")
            st.text_area("Raw Resume Text", text, height=200, help="This is the full text extracted from your PDF resume.")
            st.subheader("Detected Skills from Resume")
            if skills:
                st.success(", ".join(skills))
            else:
                st.warning("No common tech skills detected. Try another resume or check formatting.")
        else:
            st.warning("Please upload a PDF resume to proceed.")

        st.divider()
        # GitHub Analysis
        github_stats = {}
        if github_url.strip():
            with st.spinner("Analyzing your GitHub profile..."):
                github_stats = fetch_github_profile_stats(github_url)
            st.subheader("GitHub Profile Analysis")
            if "error" in github_stats:
                st.error(github_stats["error"])
            else:
                st.info(f"**Username:** {github_stats['username']}")
                st.write(f"**Public Repositories:** {github_stats['repo_count']}")
                st.write(f"**Languages Used:** {', '.join(github_stats['languages']) if github_stats['languages'] else 'None detected'}")
                st.write(f"**Project Topics:** {', '.join(github_stats['topics']) if github_stats['topics'] else 'None detected'}")
        else:
            st.info("Enter your GitHub profile URL to see GitHub analysis.")

        st.divider()
        # AI Skill Gap Report
        if skills and github_stats and "error" not in github_stats and career_goal.strip():
            with st.spinner("Generating your AI-powered skill gap report..."):
                report = generate_skill_gap_report(skills, github_stats, career_goal)
            st.subheader(f"AI Skill Gap Report 🧠")
            if "error" in report:
                st.error(f"OpenAI API Error: {report['error']}")
            else:
                st.markdown(report["report_markdown"])
                # Save to Firebase
                user_data = {
                    "resume_skills": skills,
                    "github_stats": github_stats,
                    "career_goal": career_goal,
                    "report": report["report_markdown"]
                }
                try:
                    save_user_report(user_id, user_data)
                    st.success("Your report has been saved to SkillGuardian!")
                except Exception as e:
                    st.warning(f"Could not save report: {e}")
        elif not career_goal.strip():
            st.info("Enter your target career goal to generate the AI report.")

elif page == "Dashboard":
    st.header("📊 My Reports Dashboard")
    with st.spinner("Fetching your reports from SkillGuardian..."):
        reports = get_user_reports(user_id)
    if not reports:
        st.info("No reports found for your session. Run an analysis to see your reports here!")
    else:
        MAX_REPORTS = 10
        if len(reports) > MAX_REPORTS:
            st.warning(f"Showing the {MAX_REPORTS} most recent reports. Older reports are hidden.")
        for idx, report in enumerate(reports[:MAX_REPORTS]):
            ts = report.get('timestamp')
            ts_str = format_timestamp(ts)
            expander_label = f"📝 Report {idx+1} ({ts_str}): {report.get('career_goal', 'Unknown Goal')}"
            with st.expander(expander_label):
                st.markdown(f"<span style='color:{ACCENT_COLOR};font-size:1.1rem;'>🕒 <b>Timestamp:</b> {ts_str}</span>", unsafe_allow_html=True)
                st.markdown(f"<span style='color:{PRIMARY_COLOR};font-size:1.1rem;'>🎯 <b>Career Goal:</b> {report.get('career_goal', 'N/A')}</span>", unsafe_allow_html=True)
                st.markdown(f"<b>💼 Resume Skills:</b> {', '.join(report.get('resume_skills', []))}")
                st.markdown(f"<b>🐙 GitHub Username:</b> {report.get('github_stats', {}).get('username', 'N/A')}")
                st.markdown(f"<b>🧑‍💻 GitHub Languages:</b> {', '.join(report.get('github_stats', {}).get('languages', []))}")
                st.markdown(f"<b>🏷️ GitHub Topics:</b> {', '.join(report.get('github_stats', {}).get('topics', []))}")
                st.markdown(report.get('report', 'No AI report found.')) 