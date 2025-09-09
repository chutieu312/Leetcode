#!/usr/bin/env bash
set -x

# Set the path to Git Bash
GIT_BASH="C:\Program Files\Git\git-bash.exe"

# Start Streamlit app in a new Git Bash window
"$GIT_BASH" --cd="c:/Users/canng/Leetcode/job_tech_analysis/job_market_tech_dashboard_llm" -c "source .venv/Scripts/activate && streamlit run streamlit_app.py"