# Job Market Tech Dashboard (Streamlit)

A one-click dashboard to track which technologies appear in the job descriptions you apply to—so you can prioritize study/practice based on real demand.

## Quickstart
1. Install dependencies (preferably in a virtualenv):
   ```bash
   pip install streamlit pandas
   ```
2. Run the app:
   ```bash
   streamlit run streamlit_app.py
   ```
3. In the left sidebar, paste new job descriptions and press **Add Posting**.
4. The dashboard updates counts and % based on the total postings-to-date.

## Files
- `streamlit_app.py` – the dashboard app.
- `data/alias_map.json` – synonyms mapping to canonical skills (edit to expand).
- `data/categories.json` – category for each canonical skill (edit to adjust).
- `data/jobs.csv` – postings you’ve added.
- `data/skills.csv` – normalized skills extracted from postings.

## Notes
- The initial dataset is seeded with your Microsoft Software Engineer II (Azure Specialized) posting (applied 2025-08-29).
- You can add weights (e.g., required vs preferred) later by editing how rows are written to `skills.csv` in the app.
