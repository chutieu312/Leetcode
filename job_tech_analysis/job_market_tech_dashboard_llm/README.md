
# Job Tech Analyzer — LLM-enabled (Local)
- Dynamic skill detection with an LLM fallback, caching, review queue, confidence gating.
- All data saved under `data/` locally.

## Run
```bash
source .venv/Scripts/activate
pip install -r requirements.txt
streamlit run streamlit_app.py


cd job_market_tech_dashboard_llm
python -m venv .venv
.venv\Scripts\Activate
python -m pip install --upgrade pip
pip install -r requirements.txt
streamlit run streamlit_app.py
```

## Configure the LLM
```powershell
# Windows PowerShell
setx OPENAI_API_KEY "sk-..."
# optional
setx LLM_MODEL "gpt-4o-mini"
```
Or create `.streamlit/secrets.toml` with:
```toml
OPENAI_API_KEY="sk-..."
LLM_MODEL="gpt-4o-mini"
```
