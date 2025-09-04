
import streamlit as st
import pandas as pd
import json, re, os, csv
from datetime import date, datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

st.set_page_config(page_title="Job Market Tech Dashboard", layout="wide")

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")
ALIAS_PATH = os.path.join(DATA_DIR, "alias_map.json")
CATEGORIES_PATH = os.path.join(DATA_DIR, "categories.json")
JOBS_CSV = os.path.join(DATA_DIR, "jobs.csv")
SKILLS_CSV = os.path.join(DATA_DIR, "skills.csv")

REQUIRED_HEADERS = [
    r"required", r"requirements", r"must have", r"basic qualifications", r"responsibilities"
]
PREFERRED_HEADERS = [
    r"preferred", r"preferred qualifications", r"nice to have", r"good to have", r"bonus"
]

WEIGHTS = {"required": 2.0, "preferred": 1.5, "mention": 1.0}

@st.cache_resource
def load_maps():
    with open(ALIAS_PATH, "r", encoding="utf-8") as f:
        alias_map = json.load(f)
    with open(CATEGORIES_PATH, "r", encoding="utf-8") as f:
        categories = json.load(f)
    return alias_map, categories

def extract_skills(text, alias_map):
    text_l = text.lower()
    found = {}
    for key in sorted(alias_map.keys(), key=len, reverse=True):
        pattern = r"(?<![A-Za-z0-9])" + re.escape(key) + r"(?![A-Za-z0-9])"
        m = re.search(pattern, text_l)
        if m:
            found[alias_map[key]] = m.start()
    return found

def find_header_index(text_l, headers):
    idxs = []
    for h in headers:
        m = re.search(rf"(?i)\b{h}\b", text_l)
        if m:
            idxs.append(m.start())
    return min(idxs) if idxs else None

def classify_position(pos, req_idx, pref_idx):
    if req_idx is not None and pref_idx is not None:
        if pos >= req_idx and pos < pref_idx:
            return "required"
        elif pos >= pref_idx:
            return "preferred"
        else:
            return "mention"
    elif req_idx is not None and pref_idx is None:
        return "required" if pos >= req_idx else "mention"
    elif req_idx is None and pref_idx is not None:
        return "preferred" if pos >= pref_idx else "mention"
    else:
        return "mention"

def append_job_and_skills(job_row, skills_positions, categories, jd_text):
    job_exists = os.path.exists(JOBS_CSV)
    with open(JOBS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not job_exists:
            writer.writerow(["job_id","date_applied","company","title","location","source","outcome","jd_text","segment_role","work_type","seniority"])
        writer.writerow(job_row)

    skills_exists = os.path.exists(SKILLS_CSV)
    with open(SKILLS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not skills_exists:
            writer.writerow(["job_id","date_applied","skill_canonical","category","weight","label","raw_match"])
        text_l = jd_text.lower()
        req_idx = find_header_index(text_l, REQUIRED_HEADERS)
        pref_idx = find_header_index(text_l, PREFERRED_HEADERS)
        for skill, pos in skills_positions.items():
            label = classify_position(pos, req_idx, pref_idx)
            weight = WEIGHTS[label]
            writer.writerow([job_row[0], job_row[1], skill, categories.get(skill,"Other"), weight, label, ""])

def load_data():
    if os.path.exists(JOBS_CSV):
        jobs = pd.read_csv(JOBS_CSV)
    else:
        jobs = pd.DataFrame(columns=["job_id","date_applied","company","title","location","source","outcome","jd_text","segment_role","work_type","seniority"])
    if os.path.exists(SKILLS_CSV):
        skills = pd.read_csv(SKILLS_CSV)
        if "label" not in skills.columns:
            skills["label"] = "mention"
        if "weight" not in skills.columns:
            skills["weight"] = 1.0
    else:
        skills = pd.DataFrame(columns=["job_id","date_applied","skill_canonical","category","weight","label","raw_match"])
    # Dates
    if not jobs.empty:
        jobs["date_applied"] = pd.to_datetime(jobs["date_applied"], errors="coerce").dt.date
    if not skills.empty:
        skills["date_applied"] = pd.to_datetime(skills["date_applied"], errors="coerce").dt.date
    return jobs, skills

alias_map, categories = load_maps()
st.title("📈 Job Market Tech Dashboard")

# --- Sidebar: Add Job + Filters ---
with st.sidebar:
    st.header("➕ Add Job Posting")
    company = st.text_input("Company", "")
    title = st.text_input("Title", "")
    location = st.text_input("Location", "")
    source = st.text_input("Source (e.g., LinkedIn)", "")
    dt = st.date_input("Date Applied", value=date.today())
    outcome = st.selectbox("Outcome (optional)", ["", "Applied", "Recruiter Screen", "OA", "Interview", "Offer", "Rejected"])
    segment_role = st.selectbox("Segment (role)", ["", "Backend", "SRE", "Data", "Full-Stack", "Other"])
    work_type = st.selectbox("Work type", ["", "Remote", "Hybrid", "Onsite"])
    seniority = st.selectbox("Seniority", ["", "New Grad", "SDE I", "SDE II", "Senior (SDE III+)", "Staff/Principal"])
    jd_text = st.text_area("Paste Job Description", height=220)

    st.caption("Tip: Paste the entire JD. We auto-detect skills via the alias map and weight by Required vs Preferred sections.")
    if st.button("Add Posting"):
        if company and title and jd_text.strip():
            job_id = f"{dt.isoformat()}_{company.upper().replace(' ','')}_{title.upper().replace(' ','')}"
            job_id = job_id[:120]
            positions = extract_skills(jd_text, alias_map)
            append_job_and_skills(
                [job_id, dt.isoformat(), company, title, location, source, outcome, jd_text, segment_role, work_type, seniority],
                positions,
                categories,
                jd_text
            )
            st.success(f"Added posting. Detected {len(positions)} skills.")
        else:
            st.error("Company, Title, and Job Description are required.")

st.divider()
st.subheader("Filters")
jobs, skills = load_data()

# Filter controls
seg_sel = st.multiselect("Segment (role)", options=["Backend","SRE","Data","Full-Stack","Other"], default=[])
work_sel = st.multiselect("Work type", options=["Remote","Hybrid","Onsite"], default=[])
sen_sel = st.multiselect("Seniority", options=["New Grad","SDE I","SDE II","Senior (SDE III+)","Staff/Principal"], default=[])

# Apply filters
if not jobs.empty:
    mask = pd.Series([True]*len(jobs))
    if seg_sel:
        mask &= jobs['segment_role'].isin(seg_sel)
    if work_sel:
        mask &= jobs['work_type'].isin(work_sel)
    if sen_sel:
        mask &= jobs['seniority'].isin(sen_sel)
    jobs_f = jobs[mask].copy()
else:
    jobs_f = jobs.copy()

if not skills.empty and not jobs_f.empty:
    skills_f = skills.merge(jobs_f[['job_id']], on='job_id', how='inner')
else:
    skills_f = skills.iloc[0:0].copy()

total_jobs = len(jobs_f.index)

col1, col2, col3, col4 = st.columns(4)
col1.metric("Total postings (filtered)", total_jobs)
col2.metric("Unique skills", skills_f['skill_canonical'].nunique() if not skills_f.empty else 0)
col3.metric("Unique categories", skills_f['category'].nunique() if not skills_f.empty else 0)
recent_7_start = (date.today() - timedelta(days=6))
recent_jobs = 0 if jobs_f.empty else int((pd.to_datetime(jobs_f['date_applied']) >= pd.to_datetime(recent_7_start)).sum())
col4.metric("Postings (last 7 days)", recent_jobs)

st.subheader("Skills prevalence")
if skills_f.empty or total_jobs == 0:
    st.info("No data for current filters. Add postings or adjust filters.")
else:
    # Unweighted counts
    unweighted = (skills_f.groupby('skill_canonical')
                  .job_id.nunique()
                  .reset_index(name='jobs_with_skill')
                  .sort_values('jobs_with_skill', ascending=False))
    unweighted['percent'] = (unweighted['jobs_with_skill'] / total_jobs * 100).round(1)

    # Required/Preferred weighting (per skill row)
    w_sum = (skills_f.groupby('skill_canonical')['weight']
             .sum()
             .reset_index()
             .rename(columns={'weight':'weighted_rows'}))

    # Recency weighting: exponential decay by days since applied
    st.markdown("**Recency weighting**")
    use_recency = st.checkbox("Enable recency (exponential decay)", value=True)
    half_life_days = st.slider("Half-life (days)", min_value=7, max_value=90, value=21, step=1)
    if use_recency:
        sf = skills_f.copy()
        # days since: today - date_applied
        sf['date_applied'] = pd.to_datetime(sf['date_applied'])
        sf['days_ago'] = (pd.Timestamp('today').normalize() - sf['date_applied']).dt.days.clip(lower=0).fillna(0)
        sf['recency_factor'] = (0.5) ** (sf['days_ago'] / half_life_days)
        sf['recency_weighted'] = sf['weight'] * sf['recency_factor']
        rec = (sf.groupby('skill_canonical')['recency_weighted'].sum()
               .reset_index(name='recency_weighted_sum'))
    else:
        rec = pd.DataFrame({'skill_canonical': unweighted['skill_canonical'], 'recency_weighted_sum': 0.0})

    agg = unweighted.merge(w_sum, on='skill_canonical', how='left').merge(rec, on='skill_canonical', how='left')
    agg['weighted_percent'] = (agg['weighted_rows'] / total_jobs * 100).round(1)
    if use_recency:
        agg['recency_weighted_percent'] = (agg['recency_weighted_sum'] / total_jobs * 100).round(1)
    else:
        agg['recency_weighted_percent'] = 0.0

    st.dataframe(agg, use_container_width=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        st.subheader("Top skills (unweighted jobs)")
        st.bar_chart(agg.set_index('skill_canonical')['jobs_with_skill'])
    with c2:
        st.subheader("Top skills (weighted rows)")
        st.bar_chart(agg.set_index('skill_canonical')['weighted_rows'])
    with c3:
        st.subheader("Top skills (recency-weighted)")
        st.bar_chart(agg.set_index('skill_canonical')['recency_weighted_sum'])

    st.subheader("By category (unweighted jobs)")
    # Convert to jobs-with-skill per category using unique job count per skill, then map to category prevalence
    skills_jobs = skills_f[['job_id','skill_canonical','category']].drop_duplicates()
    cat_counts = (skills_jobs.groupby('category')['job_id'].nunique()
                  .reset_index(name='jobs_with_any_skill_in_cat')
                  .sort_values('jobs_with_any_skill_in_cat', ascending=False))
    cat_counts['percent'] = (cat_counts['jobs_with_any_skill_in_cat'] / total_jobs * 100).round(1)
    st.dataframe(cat_counts, use_container_width=True)

    st.subheader("7-day trend (prevalence by day)")
    jobs_f['date_applied'] = pd.to_datetime(jobs_f['date_applied'])
    skills_f['date_applied'] = pd.to_datetime(skills_f['date_applied'])

    end = pd.Timestamp.today().normalize()
    start = end - pd.Timedelta(days=6)
    days = pd.date_range(start=start, end=end, freq='D')

    skill_options = agg['skill_canonical'].tolist()
    default_sel = skill_options[:min(5, len(skill_options))]
    selected = st.multiselect("Pick up to 5 skills to plot", options=skill_options, default=default_sel)
    selected = selected[:5]

    if selected:
        trend_df = []
        for d in days:
            day_jobs = jobs_f[jobs_f['date_applied'].dt.date == d.date()]
            total_day_jobs = max(1, len(day_jobs))
            for s in selected:
                day_skill_jobs = skills_f[(skills_f['skill_canonical'] == s) & (skills_f['date_applied'].dt.date == d.date())]['job_id'].nunique()
                pct = day_skill_jobs / total_day_jobs * 100 if total_day_jobs > 0 else 0.0
                trend_df.append({"date": d.date(), "skill": s, "percent": round(pct, 1)})
        trend_df = pd.DataFrame(trend_df)
        chart_df = trend_df.pivot(index='date', columns='skill', values='percent').fillna(0.0)
        st.line_chart(chart_df)

    st.subheader("Co-occurrence heatmap (common skill bundles)")
    # Choose top N skills by unweighted jobs
    N = st.slider("Top N skills for heatmap", min_value=5, max_value=30, value=15, step=1)
    top_skills = agg.sort_values('jobs_with_skill', ascending=False)['skill_canonical'].head(N).tolist()
    if top_skills:
        # Build job x skill binary matrix
        sj = skills_f[['job_id','skill_canonical']].drop_duplicates()
        sj = sj[sj['skill_canonical'].isin(top_skills)]
        # Pivot
        pivot = (sj.assign(val=1)
                   .pivot_table(index='job_id', columns='skill_canonical', values='val', fill_value=0))
        # Co-occurrence counts
        co = pivot.T.dot(pivot)
        st.dataframe(co, use_container_width=True)
        # Simple heatmap
        fig, ax = plt.subplots(figsize=(max(6, N*0.4), max(4, N*0.4)))
        im = ax.imshow(co.values)
        ax.set_xticks(range(len(top_skills)))
        ax.set_yticks(range(len(top_skills)))
        ax.set_xticklabels(top_skills, rotation=90)
        ax.set_yticklabels(top_skills)
        ax.set_title("Co-occurrence (number of postings containing both skills)")
        for (i, j), val in np.ndenumerate(co.values):
            ax.text(j, i, int(val), ha='center', va='center', fontsize=8)
        st.pyplot(fig)

    st.subheader("Outcome correlation (skills × outcomes)")
    if 'outcome' in jobs_f.columns and not jobs_f.empty:
        skills_jobs = skills_f.merge(jobs_f[['job_id','outcome']], on='job_id', how='left')
        skills_jobs['outcome'] = skills_jobs['outcome'].fillna("")
        positive = {"Recruiter Screen", "OA", "Interview", "Offer"}
        totals = skills_jobs.groupby('skill_canonical')['job_id'].nunique().rename('total_jobs_with_skill')
        hits = skills_jobs[skills_jobs['outcome'].isin(list(positive))].groupby('skill_canonical')['job_id'].nunique().rename('positive_jobs_with_skill')
        corr = pd.concat([totals, hits], axis=1).fillna(0).reset_index()
        corr['positive_rate_%'] = (corr['positive_jobs_with_skill'] / corr['total_jobs_with_skill'] * 100).round(1).replace([float('inf')], 0)
        st.dataframe(corr.sort_values('positive_rate_%', ascending=False), use_container_width=True)
    else:
        st.info("Add outcomes to postings to see which skills correlate with interviews/offers.")

    # --- Export buttons ---
    st.subheader("Export data")
    # Prepare CSVs
    jobs_csv_data = jobs_f.to_csv(index=False).encode("utf-8")
    skills_csv_data = skills_f.to_csv(index=False).encode("utf-8")
    agg_csv = agg.to_csv(index=False).encode("utf-8")
    cat_csv = cat_counts.to_csv(index=False).encode("utf-8")
    st.download_button("Download jobs.csv (filtered)", jobs_csv_data, file_name="jobs_filtered.csv")
    st.download_button("Download skills.csv (filtered)", skills_csv_data, file_name="skills_filtered.csv")
    st.download_button("Download skills_aggregate.csv", agg_csv, file_name="skills_aggregate.csv")
    st.download_button("Download categories_aggregate.csv", cat_csv, file_name="categories_aggregate.csv")

st.divider()
with st.expander("📤 Export to Google Sheets (how-to)"):
    st.markdown("""
**Option A (manual import):**
1. Click the **Download** buttons above to get your CSVs.
2. Open [Google Sheets](https://sheets.google.com) → **File → Import → Upload** → choose your CSV.
3. Choose **Insert new sheet(s)**.

**Option B (automated via API)**: Requires a Google Cloud service account + credentials.
1. Create a Service Account with the **Google Sheets API** enabled.
2. Download the JSON key and place it beside this app as `service_account.json` (do not commit publicly).
3. Share your Google Sheet with the service account email.
4. Install dependencies:
   ```bash
   pip install gspread google-auth
   ```
5. Sample code snippet (add to this app and secure your secrets properly):
   ```python
   import gspread
   from google.oauth2.service_account import Credentials
   scopes = ["https://www.googleapis.com/auth/spreadsheets"]
   creds = Credentials.from_service_account_file("service_account.json", scopes=scopes)
   gc = gspread.authorize(creds)
   sh = gc.open_by_key("YOUR_SHEET_ID")
   ws = sh.worksheet("skills_aggregate")  # or create it if missing
   # df is your pandas DataFrame
   ws.update([df.columns.values.tolist()] + df.values.tolist())
   ```
    """)

st.caption("Recency weighting uses exponential decay with adjustable half-life. Filters limit all calculations to the selected segments.")
