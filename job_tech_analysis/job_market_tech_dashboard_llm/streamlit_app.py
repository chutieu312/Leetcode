
import streamlit as st
import pandas as pd
import json, re, os, csv
from datetime import date

# LLM client (optional)
LLM_AVAILABLE = True
try:
    from openai import OpenAI
except Exception:
    try:
        import openai  # legacy
    except Exception:
        LLM_AVAILABLE = False

st.set_page_config(page_title="Job Tech Analyzer (LLM-enabled)", layout="wide")

BASE = os.path.dirname(__file__)
DATA_DIR = os.path.join(BASE, "data")
ALIAS_PATH = os.path.join(DATA_DIR, "alias_map.json")
CATEGORIES_PATH = os.path.join(DATA_DIR, "categories.json")
JOBS_CSV = os.path.join(DATA_DIR, "jobs.csv")
SKILLS_CSV = os.path.join(DATA_DIR, "skills.csv")
CACHE_PATH = os.path.join(DATA_DIR, "llm_cache.json")
REVIEW_Q_PATH = os.path.join(DATA_DIR, "review_queue.json")

# Step 1: Add after file path constants
IGNORE_PATH = os.path.join(DATA_DIR, "ignore_terms.json")

def load_ignores():
    return load_json(IGNORE_PATH, [])

def save_ignores(items):
    save_json(IGNORE_PATH, items)

STOPWORD_TOKENS = {
    # ...copy the full set from the suggestion...
    "A","An","And","As","About","Ability","Additional","All","Also","AND","Any","Applicant",
    "Bachelor","Background","Basic","Bonus","Check","Company","Computer","Contributes","Creates",
    "Degree","Depgree","Designated","DRI","Each","Education","Eligible","Eligibility","Engineer",
    "Experience","II","Individual","Internet","IP","Knowledge","Master","Minimum","Mission",
    "Must","Nice","OR","Other","Overview","Preferred","Qualifications","Required","Requirements",
    "Responsibilities","Responsible","Science","Software","Software-Defined","Specialized",
    "Switches","TCP","The","These","Top","Transmission","Understanding","Work","Works"
}

KNOWN_SHORT_TECH = {"C","R","Go","C#","C++","SQL","TCP/IP","SDN"}

CONTEXT_TRIGGERS = {
    # ...copy the full set from the suggestion...
    "experience with","proficient in","knowledge of","familiar with","using",
    "worked with","hands-on","expertise in","implement","design","build",
    "deploy","monitor","observability","pipeline","ci/cd","infrastructure",
    "sdn","tcp/ip","database","databases","kubernetes","cloud","aws","azure","gcp"
}

def has_context_near(text_l: str, token: str, window_words: int = 8) -> bool:
    # Find first occurrence; look ±window for triggers
    m = re.search(re.escape(token), text_l, flags=re.I)
    if not m: 
        return False
    start = m.start()
    # crude word window
    left = max(0, start - 300)
    window = text_l[left:start+300]
    return any(t in window for t in CONTEXT_TRIGGERS)

REQUIRED_HEADERS = [r"required", r"requirements", r"must have", r"basic qualifications", r"responsibilities"]
PREFERRED_HEADERS = [r"preferred", r"preferred qualifications", r"nice to have", r"good to have", r"bonus"]
WEIGHTS = {"required": 2.0, "preferred": 1.5, "mention": 1.0}

CATEGORIES = [
    "Programming Language","Runtime/Framework","Frontend Framework",
    "Database","Data Warehouse","Caching","Search/Analytics",
    "Cloud Platform","Cloud Service",
    "Containers","Container Orchestration",
    "CI/CD","IaC",
    "Observability","Security",
    "Streaming","Messaging",
    "Web/API",
    "Orchestration","Workflow",
    "Big Data/Analytics","ML/AI",
    "Networking","Storage",
    "SRE","Other","Unknown"
]

REGEX_ALIASES = [
    (r"\bgolang\b", "Go"),
    (r"\bgo\s+language\b", "Go"),
    (r"\bnode\.js\b|\bnodejs\b", "Node.js"),
    (r"\btypescript\b", "TypeScript"),
    (r"\bgraphql\b|\bgraph\s*q\s*l\b", "GraphQL"),
    (r"\bk8s\b", "Kubernetes"),
    (r"\bgoogle\s+cloud(?:\s+platform)?\b", "GCP"),
]

def load_json(path, default):
    try:
        with open(path, "r", encoding="utf-8") as f: 
            return json.load(f)
    except Exception:
        return default

def save_json(path, data):
    with open(path, "w", encoding="utf-8") as f: 
        json.dump(data, f, indent=2, ensure_ascii=False)

def load_maps():
    return load_json(ALIAS_PATH, {}), load_json(CATEGORIES_PATH, {})

def save_maps(alias_map, categories):
    save_json(ALIAS_PATH, alias_map); 
    save_json(CATEGORIES_PATH, categories)

def find_header_index(text_l, headers):
    idxs = []
    for h in headers:
        m = re.search(rf"(?i)\b{h}\b", text_l)
        if m: idxs.append(m.start())
    return min(idxs) if idxs else None

def classify_position(pos, req_idx, pref_idx):
    if req_idx is not None and pref_idx is not None:
        if pos >= req_idx and pos < pref_idx: return "required"
        elif pos >= pref_idx: return "preferred"
        else: return "mention"
    elif req_idx is not None: return "required" if pos >= req_idx else "mention"
    elif pref_idx is not None: return "preferred" if pos >= pref_idx else "mention"
    return "mention"

def cheap_candidates(jd_text):
    """
    Extract candidate tech terms while filtering out common non-tech words.
    - Keeps ProperCase tokens, ALLCAPS, and things like NoSQL/SQL.
    - Drops sentence-starter fluff (STOPWORD_TOKENS).
    - Drops 1–2 letter tokens unless white-listed in KNOWN_SHORT_TECH.
    - Prefers tokens that appear near tech-y context words.
    """
    text_l = jd_text.lower()

    # 1) raw candidates (single tokens)
    raw = set()
    for m in re.finditer(r"\b([A-Z][a-zA-Z0-9+\#\.\-]{1,}|[A-Z]{2,}|[a-zA-Z]+SQL|NoSQL)\b", jd_text):
        tok = m.group(0).strip()
        raw.add(tok)

    # 2) light pass for multi-word tech phrases (e.g., "Software Defined Networking", "Top of Rack")
    for m in re.finditer(r"\b([A-Z][\w\+\#\.\-]*(?:\s+(?:of|and|for|to|in|on|as|with))?\s+[A-Z][\w\+\#\.\-]*)\b", jd_text):
        phrase = m.group(0).strip()
        if len(phrase.split()) <= 5:  # keep short phrases only
            raw.add(phrase)

    # 3) filter junk
    kept = set()
    ignores = set(load_ignores())
    for tok in raw:
        if tok in ignores:
            continue
        if tok in STOPWORD_TOKENS:
            continue
        if len(tok) <= 2 and tok not in KNOWN_SHORT_TECH:
            continue
        # Sentence starters like "About", "Ability" often appear capitalized but not tech
        if tok.istitle() and tok.lower() not in {"mysql","mongodb","postgresql"} and not has_context_near(text_l, tok):
            # if it doesn't sit near context, skip it
            continue
        kept.add(tok)

    return kept


def alias_pass(jd_text, alias_map):
    text_l = jd_text.lower()
    found = {}
    for key in sorted(alias_map.keys(), key=len, reverse=True):
        pattern = r"(?<![A-Za-z0-9])" + re.escape(key) + r"(?![A-Za-z0-9])"
        for m in re.finditer(pattern, text_l):
            can = alias_map[key]
            found[can] = min(found.get(can, m.start()), m.start())
    for pat, can in REGEX_ALIASES:
        for m in re.finditer(pat, text_l):
            found[can] = min(found.get(can, m.start()), m.start())
    return found

def get_llm_client():
    api_key = os.getenv("OPENAI_API_KEY", st.secrets.get("OPENAI_API_KEY", ""))
    model = os.getenv("LLM_MODEL", st.secrets.get("LLM_MODEL", "gpt-4o-mini"))
    if not api_key:
        return None, None
    try:
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        return client, model
    except Exception:
        try:
            import openai
            openai.api_key = api_key
            return openai, model
        except Exception:
            return None, None

CATEGORIES_LIST_STR = ", ".join(CATEGORIES)

def llm_classify_unknowns(terms, jd_text, cache, temperature=0.0):
    client, model = get_llm_client()
    results = {}
    to_query = []
    for t in terms:
        if t.lower() in cache:
            results[t] = cache[t.lower()]
        else:
            to_query.append(t)
    if not to_query:
        return results, cache, []

    if not client:
        for t in to_query:
            results[t] = {"term": t, "canonical_name": t, "category":"Unknown", "vendor": None, "synonyms": [], "confidence": 0.0, "reason":"LLM not configured"}
        return results, cache, to_query

    prompt = f"""
You are an information extractor for job descriptions. 
For each term below that appears to be a technology/tool/framework/service, return a JSON object:
{{
  "items": [{{"term": "...", "canonical_name": "...", "category": "<one of [{CATEGORIES_LIST_STR}]>", "vendor": "<or null>", "synonyms": ["..."], "confidence": 0.0-1.0, "reason": "..." }}, ...]
}}
If a term is NOT a technology/tool/service, return it with category "Unknown" and confidence 0.

JD (snippet for context):
\"\"\"{jd_text[:4000]}\"\"\"

TERMS:
{to_query}
"""
    try:
        raw = "{}"
        try:
            from openai import OpenAI
            if isinstance(client, OpenAI):
                resp = client.chat.completions.create(
                    model=model,
                    temperature=temperature,
                    messages=[
                        {"role":"system","content":"Return strict JSON only. No prose."},
                        {"role":"user","content": prompt}
                    ],
                    response_format={"type":"json_object"}
                )
                raw = resp.choices[0].message.content
            else:
                raw = client.ChatCompletion.create(
                    model=model,
                    temperature=temperature,
                    messages=[
                        {"role":"system","content":"Return strict JSON only. No prose."},
                        {"role":"user","content": prompt}
                    ]
                )["choices"][0]["message"]["content"]
        except Exception:
            pass
        data = json.loads(raw) if isinstance(raw, str) else {}
        items = data.get("items", [])
        by_term = { (it.get("term") or it.get("canonical_name") or "").strip(): it for it in items }
        for t in to_query:
            it = by_term.get(t) or {"term":t,"canonical_name":t,"category":"Unknown","vendor":None,"synonyms":[],"confidence":0.0,"reason":"Parse failure"}
            results[t] = it
            cache[t.lower()] = it
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        return results, cache, to_query
    except Exception as e:
        for t in to_query:
            results[t] = {"term": t, "canonical_name": t, "category":"Unknown", "vendor": None, "synonyms": [], "confidence": 0.0, "reason": f"LLM error: {e}"}
            cache[t.lower()] = results[t]
        with open(CACHE_PATH, "w", encoding="utf-8") as f:
            json.dump(cache, f, indent=2, ensure_ascii=False)
        return results, cache, to_query

def extract_with_llm_fallback(jd_text, alias_map, categories, conf_threshold=0.75):
    """
    Extract skills with alias/regex first, then use LLM for unknowns.
    Tightened gating: require tech context (unless token is tech-shaped),
    drop very-low-confidence unknowns, and only queue meaningful items.
    """
    cache = load_json(CACHE_PATH, {})
    review_q = load_json(REVIEW_Q_PATH, [])

    # 1) Known mappings & regex aliases
    found = alias_pass(jd_text, alias_map)
    cands = cheap_candidates(jd_text)
    text_l = jd_text.lower()

    # 2) Build unknown list (not already found/aliased), with context guard
    unknowns = []
    for tok in sorted(cands, key=str.lower):
        if tok in found:
            continue
        if tok.lower() in alias_map:
            continue
        if tok == "Go" and not re.search(r"\bgolang\b", text_l):
            continue
        # Require context unless obviously tech-shaped (contains digits/+/# or ends with SQL)
        tech_shaped = bool(re.search(r"(SQL$|NoSQL$|[+#\d])", tok))
        if not tech_shaped and not has_context_near(text_l, tok):
            continue
        unknowns.append(tok)

    # 3) LLM classification
    llm_results, cache, asked = llm_classify_unknowns(unknowns, jd_text, cache)

    # 4) Accept / ignore / queue
    learned = []
    LOW_CONF_DROP = 0.30  # anything below this = silently ignore (no queue)
    for tok in unknowns:
        info = llm_results.get(tok, {"canonical_name": tok, "category": "Unknown", "confidence": 0.0, "synonyms": []})
        canon = info.get("canonical_name", tok).strip()
        cat = (info.get("category") or "Unknown").strip()
        conf = float(info.get("confidence") or 0.0)

        if conf >= conf_threshold and cat != "Unknown":
            # Auto-accept & learn
            alias_map[tok.lower()] = canon
            if canon not in categories:
                categories[canon] = cat
            pos = jd_text.find(tok)
            if pos == -1:
                pos = 0
            found[canon] = min(found.get(canon, pos), pos)
            learned.append({"term": tok, "canonical_name": canon, "category": categories[canon], "confidence": conf})
        elif conf < LOW_CONF_DROP and cat == "Unknown":
            # Do not clutter the queue with obvious non-tech; persist ignore so it won't recur
            ignores = set(load_ignores())
            ignores.add(tok)
            save_ignores(sorted(ignores))
        else:
            # Queue for review (avoid duplicate pending items)
            exists = any(q.get("term", "").lower() == tok.lower() and q.get("status") == "pending" for q in review_q)
            if not exists:
                review_q.append({
                    "term": tok,
                    "suggested": {
                        "canonical_name": canon,
                        "category": cat,
                        "confidence": conf,
                        "synonyms": info.get("synonyms", []),
                        "reason": info.get("reason", "")
                    },
                    "status": "pending"
                })

    # 5) Persist maps & queue and return results
    save_maps(alias_map, categories)
    save_json(REVIEW_Q_PATH, review_q)
    return found, learned


def append_job_and_skills(job_row, jd_text, alias_map, categories, conf_threshold):
    text_l = jd_text.lower()
    req_idx = find_header_index(text_l, REQUIRED_HEADERS)
    pref_idx = find_header_index(text_l, PREFERRED_HEADERS)

    positions, learned = extract_with_llm_fallback(jd_text, alias_map, categories, conf_threshold=conf_threshold)

    # Write job
    job_exists = os.path.exists(JOBS_CSV)
    with open(JOBS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not job_exists:
            writer.writerow(["job_id","date_applied","company","title","location","source","outcome","jd_text","segment_role","work_type","seniority"])
        writer.writerow(job_row)

    # Write skills
    skills_exists = os.path.exists(SKILLS_CSV)
    with open(SKILLS_CSV, "a", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        if not skills_exists:
            writer.writerow(["job_id","date_applied","skill_canonical","category","weight","label","raw_match"])
        for can, pos in positions.items():
            label = classify_position(pos, req_idx, pref_idx)
            weight = WEIGHTS[label]
            writer.writerow([job_row[0], job_row[1], can, categories.get(can,"Unknown"), weight, label, ""])
    return learned

def load_data():
    if os.path.exists(JOBS_CSV):
        jobs = pd.read_csv(JOBS_CSV)
    else:
        jobs = pd.DataFrame(columns=["job_id","date_applied","company","title","location","source","outcome","jd_text","segment_role","work_type","seniority"])
    if os.path.exists(SKILLS_CSV):
        skills = pd.read_csv(SKILLS_CSV)
        if "label" not in skills.columns: skills["label"]="mention"
        if "weight" not in skills.columns: skills["weight"]=1.0
    else:
        skills = pd.DataFrame(columns=["job_id","date_applied","skill_canonical","category","weight","label","raw_match"])
    if not jobs.empty:
        jobs["date_applied"] = pd.to_datetime(jobs["date_applied"], errors="coerce").dt.date
    if not skills.empty:
        skills["date_applied"] = pd.to_datetime(skills["date_applied"], errors="coerce").dt.date
    return jobs, skills

st.title("📈 Job Tech Analyzer — LLM-enabled (Local)")

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

    st.caption("LLM fallback auto-detects new skills and classifies them. Set OPENAI_API_KEY (and optional LLM_MODEL).")

    conf_threshold = st.slider("Auto-accept confidence threshold", 0.5, 0.95, 0.75, 0.01)

    if st.button("Add Posting"):
        if company and title and jd_text.strip():
            job_id = f"{dt.isoformat()}_{company.upper().replace(' ','')}_{title.upper().replace(' ','')}"
            job_id = job_id[:120]
            alias_map, categories = load_maps()
            learned = append_job_and_skills(
                [job_id, dt.isoformat(), company, title, location, source, outcome, jd_text, segment_role, work_type, seniority],
                jd_text, alias_map, categories, conf_threshold
            )
            if learned:
                st.success("Added posting. Auto-learned: " + ", ".join([f"{x['term']}→{x['canonical_name']} ({x['category']}, {x['confidence']:.2f})" for x in learned]))
            else:
                st.success("Added posting.")
        else:
            st.error("Company, Title, and Job Description are required.")

st.divider()
st.subheader("Filters")
jobs, skills = load_data()
seg_sel = st.multiselect("Segment (role)", options=["Backend","SRE","Data","Full-Stack","Other"], default=[])
work_sel = st.multiselect("Work type", options=["Remote","Hybrid","Onsite"], default=[])
sen_sel = st.multiselect("Seniority", options=["New Grad","SDE I","SDE II","Senior (SDE III+)", "Staff/Principal"], default=[])

if not jobs.empty:
    mask = pd.Series([True]*len(jobs))
    if seg_sel: mask &= jobs['segment_role'].isin(seg_sel)
    if work_sel: mask &= jobs['work_type'].isin(work_sel)
    if sen_sel: mask &= jobs['seniority'].isin(sen_sel)
    jobs_f = jobs[mask].copy()
else:
    jobs_f = jobs.copy()

if not skills.empty and not jobs_f.empty:
    skills_f = skills.merge(jobs_f[['job_id']], on='job_id', how='inner')
else:
    skills_f = skills.iloc[0:0].copy()

total_jobs = len(jobs_f.index)

c1, c2, c3 = st.columns(3)
c1.metric("Total postings (filtered)", total_jobs)
c2.metric("Unique skills", skills_f['skill_canonical'].nunique() if not skills_f.empty else 0)
c3.metric("Unique categories", skills_f['category'].nunique() if not skills_f.empty else 0)

st.subheader("Skills prevalence (unweighted & weighted)")
if skills_f.empty or total_jobs == 0:
    st.info("No data for current filters.")
else:
    unweighted = (skills_f.groupby('skill_canonical').job_id.nunique().reset_index(name='jobs_with_skill'))
    unweighted['percent'] = (unweighted['jobs_with_skill'] / total_jobs * 100).round(1)
    weighted = (skills_f.groupby('skill_canonical')['weight'].sum().reset_index().rename(columns={'weight':'weighted_rows'}))
    agg = pd.merge(unweighted, weighted, on='skill_canonical', how='left').sort_values('jobs_with_skill', ascending=False)
    agg['weighted_percent'] = (agg['weighted_rows'] / total_jobs * 100).round(1)
    st.dataframe(agg, use_container_width=True)
    st.bar_chart(agg.set_index('skill_canonical')['jobs_with_skill'])
    
    
# --- Job report ---
st.divider()
st.subheader("📄 Job report")

# Session state defaults
st.session_state.setdefault("jr_open", False)
st.session_state.setdefault("jr_order", "Newest first")
st.session_state.setdefault("jr_use_date", False)

def _toggle_report():
    st.session_state.jr_open = not st.session_state.jr_open

def _show_report():
    st.session_state.jr_open = True

# Compute date bounds from data (safe if empty)
if jobs.empty or jobs["date_applied"].isna().all():
    min_date = max_date = date.today()
else:
    min_date = min(j for j in jobs["date_applied"] if pd.notna(j))
    max_date = max(j for j in jobs["date_applied"] if pd.notna(j))

# Controls
c1, c2, c3, c4 = st.columns([1.1, 0.9, 1.2, 0.9])

with c1:
    st.session_state.jr_order = st.radio(
        "Order",
        ["Oldest first", "Newest first"],
        horizontal=True,
        index=1,  # default: Newest first
        on_change=_show_report,
        key="jr_order_radio",
    )
    # Keep a simple string in jr_order for readability
    st.session_state.jr_order = st.session_state.jr_order_radio

with c2:
    st.session_state.jr_use_date = st.checkbox(
        "Filter by date range",
        value=False,  # default: OFF
        on_change=_show_report,
        key="jr_use_date_chk",
    )

# Date pickers (only show when enabled)
with c3:
    if st.session_state.jr_use_date:
        st.session_state.setdefault("jr_start", min_date)
        st.date_input(
            "Start date",
            value=st.session_state.jr_start,
            min_value=min_date,
            max_value=max_date,
            key="jr_start",
            on_change=_show_report,
        )
    else:
        st.write("")  # spacer

with c4:
    if st.session_state.jr_use_date:
        st.session_state.setdefault("jr_end", max_date)
        st.date_input(
            "End date",
            value=st.session_state.jr_end,
            min_value=min_date,
            max_value=max_date,
            key="jr_end",
            on_change=_show_report,
        )
    else:
        st.write("")  # spacer

# Toggle button
st.button("Job report", help="Show / hide the job report", on_click=_toggle_report)

# Render (or hide) the report
if st.session_state.jr_open:
    if jobs.empty:
        st.info("No jobs recorded yet.")
    else:
        # Build working frame with needed columns (+ ids & jd for toggling)
        df = jobs[["job_id", "company", "title", "work_type", "date_applied", "source", "jd_text"]].copy()

        # Optional date filtering (only if enabled)
        if st.session_state.jr_use_date:
            start = st.session_state.get("jr_start", min_date)
            end   = st.session_state.get("jr_end", max_date)
            if start > end:
                start, end = end, start
            df = df[(df["date_applied"] >= start) & (df["date_applied"] <= end)]

        # Sort (default: Newest first)
        ascending = (st.session_state.jr_order == "Oldest first")
        df = df.sort_values("date_applied", ascending=ascending, kind="mergesort").reset_index(drop=True)

        # Add running number in display order
        df.insert(0, "number", range(1, len(df) + 1))

        # --- Interactive tabular render with clickable Title toggle ---
        # Prepare per-row open state store
        if "jr_row_open" not in st.session_state:
            st.session_state.jr_row_open = {}

        # Header row
        h1, h2, h3, h4, h5, h6 = st.columns([0.6, 1.5, 2.2, 1.2, 1.2, 1.4])
        h1.markdown("**#**")
        h2.markdown("**Company**")
        h3.markdown("**Title (click to toggle JD)**")
        h4.markdown("**Work type**")
        h5.markdown("**Date applied**")
        h6.markdown("**Source**")

        # Rows
        for _, r in df.iterrows():
            job_id = str(r["job_id"])
            st.session_state.jr_row_open.setdefault(job_id, False)

            c1, c2, c3, c4, c5, c6 = st.columns([0.6, 1.5, 2.2, 1.2, 1.2, 1.4])
            c1.write(int(r["number"]))
            c2.write(r["company"])

            # Title as a toggle button
            if c3.button(str(r["title"]), key=f"jr_title_{job_id}"):
                st.session_state.jr_row_open[job_id] = not st.session_state.jr_row_open[job_id]

            c4.write(r["work_type"] if pd.notna(r["work_type"]) and r["work_type"] != "" else "-")
            # Ensure date prints nicely even if dtype is object
            date_val = r["date_applied"]
            try:
                date_str = pd.to_datetime(date_val).date().isoformat()
            except Exception:
                date_str = str(date_val)
            c5.write(date_str)
            c6.write(r["source"] if pd.notna(r["source"]) and r["source"] != "" else "-")

            # Conditional JD render below the row
            if st.session_state.jr_row_open[job_id]:
                # Slight indent via empty column + container
                _, jd_col = st.columns([0.6, 5.5])
                with jd_col:
                    st.markdown(
                        "<div style='padding:10px; border:1px solid #e5e7eb; border-radius:8px;'>"
                        "<b>Job Description</b></div>",
                        unsafe_allow_html=True,
                    )
                    st.text(r["jd_text"] or "")
                st.markdown("")  # spacer line


st.divider()
with st.expander("🧰 Review queue (low-confidence detections)"):
    review_q = load_json(REVIEW_Q_PATH, [])
    alias_map, categories = load_maps()
    # Build category options dynamically from the fixed taxonomy + anything already used
    existing_cats = sorted(set(CATEGORIES) | set(categories.values()))
    cat_options = existing_cats + ["+ Add new category…"]
    if not review_q:
        st.success("No pending items.")
    else:
        new_items = []
        for idx, item in enumerate(review_q):
            if item.get("status") != "pending": 
                new_items.append(item)
                continue
            col = st.container()
            sug = item.get("suggested", {})
            with col:
                st.write(f"**{item['term']}** — suggested: {sug.get('canonical_name','?')} | {sug.get('category','Unknown')} (conf {sug.get('confidence',0):.2f})")
                canon = st.text_input(f"Canonical name #{idx}", value=sug.get("canonical_name",""), key=f"canon_{idx}")
                # Category selector with "Add new…" affordance
                try:
                    default_idx = cat_options.index(sug.get("category","Unknown")) if sug.get("category","Unknown") in cat_options else cat_options.index("Other")
                except Exception:
                    default_idx = cat_options.index("Other")
                selected_cat = st.selectbox(
                    f"Category #{idx}",
                    options=cat_options,
                    index=default_idx,
                    key=f"cat_{idx}",
                )
                # If user wants a new category, show a text input
                new_cat_key = f"new_cat_{idx}"
                if selected_cat == "+ Add new category…":
                    st.session_state.setdefault(new_cat_key, "")
                    new_cat_value = st.text_input("New category name", key=new_cat_key, placeholder="e.g., Quality/Testing")
                else:
                    new_cat_value = ""
                cols = st.columns(4)
                accept = cols[0].button("Accept", key=f"acc_{idx}")
                skip   = cols[1].button("Skip",   key=f"skip_{idx}")
                delete = cols[2].button("Delete", key=f"del_{idx}")
                ignore = cols[3].button("Ignore term", key=f"ign_{idx}")
                # --- Accept logic with new-category support ---
                def _normalize_cat(name: str) -> str:
                    return name.strip()
                if accept:
                    # Resolve final category
                    final_cat = _normalize_cat(new_cat_value) if selected_cat == "+ Add new category…" and new_cat_value.strip() else selected_cat
                    # Guardrails: fall back to "Other" if blank
                    if not final_cat or final_cat == "+ Add new category…":
                        final_cat = "Other"
                    # Persist alias and category
                    alias_map[item['term'].lower()] = canon or item['term']
                    if (canon or item['term']) not in categories:
                        categories[canon or item['term']] = final_cat
                    # Also expand dynamic taxonomy so the new category appears in pickers immediately
                    if final_cat not in CATEGORIES and final_cat not in existing_cats:
                        existing_cats.append(final_cat)
                    item["status"] = "accepted"
                    save_maps(alias_map, categories)
                elif skip:
                    item["status"] = "skipped"
                elif delete:
                    item["status"] = "deleted"
                elif ignore:
                    ig = set(load_ignores())
                    ig.add(item["term"])
                    save_ignores(sorted(ig))
                    item["status"] = "ignored"
            new_items.append(item)
        save_json(REVIEW_Q_PATH, new_items)
        st.info("Changes saved. Accepted items are added to alias/categories for future parsing. (Use 'Rebuild' below to re-parse older JDs.)")

st.divider()
with st.expander("🧹 Maintenance: rebuild skills from jobs.csv (uses cache + LLM for unknowns)"):
    st.write("If you changed aliases/categories or accepted items from the review queue, use this to re-parse all historical JDs. Cached LLM results will be reused.")
    conf_threshold = st.slider("Confidence threshold for auto-accept (rebuild)", 0.5, 0.95, 0.75, 0.01, key="rebuild_thr")
    if st.button("Rebuild now"):
        alias_map, categories = load_maps()
        jobs_df = pd.read_csv(JOBS_CSV) if os.path.exists(JOBS_CSV) else pd.DataFrame(columns=["job_id","date_applied","jd_text"])
        rows = []
        for _, row in jobs_df.iterrows():
            jd = str(row.get("jd_text",""))
            positions, learned = extract_with_llm_fallback(jd, alias_map, categories, conf_threshold=conf_threshold)
            text_l = jd.lower()
            req_idx = find_header_index(text_l, REQUIRED_HEADERS)
            pref_idx = find_header_index(text_l, PREFERRED_HEADERS)
            for can, pos in positions.items():
                label = classify_position(pos, req_idx, pref_idx)
                weight = WEIGHTS[label]
                rows.append([row['job_id'], row['date_applied'], can, categories.get(can,"Unknown"), weight, label, ""])
        cols = ["job_id","date_applied","skill_canonical","category","weight","label","raw_match"]
        pd.DataFrame(rows, columns=cols).to_csv(SKILLS_CSV, index=False)
        st.success("Rebuilt skills.csv")

st.caption("Set OPENAI_API_KEY (and optional LLM_MODEL) to enable LLM fallback. Cache: data/llm_cache.json; Review queue: data/review_queue.json.")
