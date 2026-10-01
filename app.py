
import os, json, re
from datetime import datetime, timezone
from pathlib import Path
import pandas as pd
import streamlit as st

st.set_page_config(page_title="Weekly CISO Targeting Engine", page_icon="🎯", layout="wide")

DATA = Path(__file__).parent / "accounts.csv"

@st.cache_data
def load_data():
    return pd.read_csv(DATA)

df = load_data()

# ---------- Styling ----------
st.markdown("""
<style>
.main {background:#f6f8fc;}
.block-container {padding-top:1.5rem; max-width:1450px;}
.hero {padding:24px 28px; border-radius:18px; background:linear-gradient(135deg,#071a3a 0%,#123b72 55%,#176b87 100%); color:white; margin-bottom:18px;}
.hero h1 {margin:0; font-size:32px;}
.hero p {margin:8px 0 0; color:#dbeafe; font-size:15px;}
.card {background:white; border:1px solid #e5eaf2; border-radius:15px; padding:18px; box-shadow:0 4px 18px rgba(16,24,40,.05);}
.rank {font-size:13px; font-weight:700; color:#64748b; text-transform:uppercase; letter-spacing:.08em;}
.score {font-size:30px; font-weight:800; color:#0f766e;}
.muted {color:#64748b;}
.small {font-size:13px;}
.pill {display:inline-block; padding:5px 9px; border-radius:999px; background:#eef6ff; color:#155e75; font-size:12px; font-weight:700;}
</style>
""", unsafe_allow_html=True)

st.markdown("""
<div class="hero">
<h1>🎯 Weekly CISO Targeting Engine</h1>
<p>AI-assisted prioritisation of enterprise cybersecurity accounts across Mumbai, Pune and Ahmedabad.</p>
</div>
""", unsafe_allow_html=True)

# Sidebar controls
st.sidebar.header("Targeting Controls")
cities = st.sidebar.multiselect("HQ city", ["Mumbai","Pune","Ahmedabad"], default=["Mumbai","Pune","Ahmedabad"])
opp_filter = st.sidebar.multiselect("Cyble opportunity", ["Threat Intelligence","Dark Web Monitoring","Brand Protection","ASM","Takedowns"], default=[])
min_signal = st.sidebar.slider("Minimum opportunity score", 0, 100, 0)

work = df[df["HQ City"].isin(cities)].copy()
if opp_filter and "Opportunity" in work:
    work = work[work["Opportunity"].fillna("").apply(lambda x: any(o.lower() in x.lower() for o in opp_filter))]
work["Opportunity Score"] = pd.to_numeric(work["Opportunity Score"], errors="coerce").fillna(0)
work = work[work["Opportunity Score"] >= min_signal].sort_values("Opportunity Score", ascending=False)

# KPIs
c1,c2,c3,c4 = st.columns(4)
c1.metric("Target Universe", len(work))
c2.metric("Weekly Targets", min(3, len(work)))
c3.metric("Cities", len(cities))
c4.metric("Last refresh", datetime.now().strftime("%d %b %Y"))

st.markdown("## 🔥 This Week’s Top 3")
top3 = work.head(3)

if len(top3) == 0:
    st.info("No accounts meet the current filters.")
else:
    cols = st.columns(3)
    for i, (_, r) in enumerate(top3.iterrows()):
        with cols[i]:
            score = int(round(r["Opportunity Score"]))
            st.markdown(f"""
            <div class="card">
              <div class="rank">Priority #{i+1}</div>
              <h2 style="margin:5px 0 2px">{r['Company']}</h2>
              <div class="muted">{r['HQ City']} · {r['Domain']}</div>
              <div style="margin-top:14px"><span class="score">{score}</span><span class="muted"> / 100 opportunity score</span></div>
              <p><b>CISO:</b> {r['CISO'] or 'Refresh intelligence to identify'}</p>
              <p><b>Cyble opportunity:</b> {r['Opportunity'] or 'To be determined'}</p>
              <p><b>Why now:</b> {r['Why Now'] or 'No current intelligence loaded yet.'}</p>
            </div>
            """, unsafe_allow_html=True)

st.markdown("## Account Intelligence")
selected = st.selectbox("Select an account", work["Company"].tolist() if len(work) else ["No accounts"])
if len(work):
    r = work[work["Company"] == selected].iloc[0]
    left,right = st.columns([1,1])
    with left:
        st.markdown("### CISO & Contact")
        st.write(f"**CISO:** {r['CISO'] or 'Not yet identified'}")
        st.write(f"**Public business contact:** {r['Public Business Contact'] or 'Not yet identified'}")
        st.write(f"**Domain:** {r['Domain']}")
        st.write(f"**HQ:** {r['HQ City']}")
        st.markdown("### Recommended Cyble conversation")
        st.info(r["Opportunity"] or "Refresh intelligence to map the opportunity.")
    with right:
        st.markdown("### Why this account?")
        st.write(r["Why Now"] or "No current evidence loaded.")
        st.markdown("### Evidence")
        st.write(r["Evidence"] or "Evidence will appear after the intelligence refresh.")
        st.caption("Use only publicly available professional contact information. Do not store private/personal phone numbers.")

st.markdown("## 📊 Top 100 Account Universe")
show = work[["Company","HQ City","CISO","Company Size Score","Cyber Signal Score","Threat Exposure Score","Security Investment Score","Opportunity Score","Opportunity"]].copy()
show.columns = ["Company","HQ","CISO","Size","Cyber Signal","Threat Exposure","Security Investment","Opportunity Score","Cyble Opportunity"]
st.dataframe(show, use_container_width=True, hide_index=True)

st.markdown("## 🧠 Scoring Model")
st.write("""
**Company Size:** 50% revenue + 50% market capitalisation, normalised across the eligible universe.

**Weekly Opportunity:** cybersecurity activity 20%, threat exposure 20%, brand/impersonation exposure 15%, security technology investment 15%, CISO activity 10%, digital expansion 10%, recent incident 10%.

The dashboard deliberately separates company size from current buying signals, so a large enterprise does not automatically become a weekly target.
""")

st.markdown("## 🔄 Intelligence Refresh")
st.warning("""
The starter dashboard is ready, but live web intelligence requires a deployed search/AI provider. 
Set the provider credentials in your deployment environment, then implement the `refresh_intelligence()` connector to populate CISO, evidence, cyber signals, and current opportunity data.
""")

st.download_button("Download current account data", df.to_csv(index=False), "ciso_accounts.csv", "text/csv")
