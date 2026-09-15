import hmac
import os

import streamlit as st

st.set_page_config(page_title="D7 Retention Explorer", page_icon="📈", layout="wide", initial_sidebar_state="collapsed")

APP_TITLE = "D7 Retention Explorer"
APP_AREA = "ANALYTICAL AI · PRODUCT MANAGEMENT & GROWTH"
APP_SUBTITLE = "Explore how early product-experience signals relate to seven-day retention."
COEFFICIENTS = {"Intercept": 0.1941, "Onboarding completion": 0.0466, "Push opt-in": 0.0604, "Week 1 sessions": 0.1931}

st.markdown("""
<style>
:root{--navy:#123b70;--teal:#19a7a8;--ink:#17324d;--muted:#647f9d;--line:#dbe7f3}
.stApp{background:#f3f9ff;color:var(--ink)}.block-container{max-width:1380px;padding:1.35rem 2.2rem 2rem}header[data-testid="stHeader"]{background:transparent}#MainMenu,footer{visibility:hidden}
.hero{padding:.35rem .4rem 1rem}.eyebrow{font-size:.76rem;font-weight:800;letter-spacing:.16em;color:#2670b8}.hero h1{font-size:clamp(2rem,3vw,2.8rem);line-height:1.05;color:#082b61;letter-spacing:-.035em;margin:.4rem 0}.hero p{font-size:1.03rem;color:#587596;margin:0}
.notice{margin:.1rem .4rem 1rem;padding:.7rem .95rem;border-left:4px solid #2670b8;border-radius:8px;background:#eaf4ff;color:#365d82;font-size:.88rem}.notice strong{color:#123b70}
.access{text-align:center;padding:.4rem 0 .8rem}.access h1{font-size:2rem;color:#082b61;margin:.3rem 0}.access p{color:#65809d}.access-note{text-align:center;color:#7890a8;font-size:.78rem;margin-top:.75rem}
[data-testid="stVerticalBlockBorderWrapper"]{background:rgba(255,255,255,.97);border:1px solid #dce8f4!important;border-radius:18px!important;box-shadow:0 10px 30px rgba(18,59,112,.07)}
.section-title{font-size:1.32rem;font-weight:800;color:#092f66}.section-copy{color:#65809d;margin:.15rem 0 .9rem}.result-card{padding:1.15rem;border-radius:14px;background:#eefafc;border:1px solid #d8f0f1}.result-label{font-size:.78rem;font-weight:800;letter-spacing:.08em;color:#53809a;text-transform:uppercase}.result-value{font-size:2.7rem;font-weight:850;color:#087f89;line-height:1.1;margin:.35rem 0}.footer{border-top:1px solid #dbe7f3;margin-top:1.5rem;padding-top:1rem;color:#6d849b;font-size:.82rem}
div.stButton>button[kind="primary"]{background:#13a4aa;border:0;border-radius:10px;min-height:3rem;font-weight:750}div.stButton>button[kind="primary"]:hover{background:#0b9299;border:0}
@media(max-width:800px){.block-container{padding:1rem}}
</style>
""", unsafe_allow_html=True)

def require_access():
    if st.session_state.get("class_access_granted", False): return
    expected = st.secrets.get("STUDENT_ACCESS_CODE", os.getenv("STUDENT_ACCESS_CODE", ""))
    _, gate, _ = st.columns([1, 1.15, 1])
    with gate:
        with st.container(border=True):
            st.markdown(f'<div class="access"><div class="eyebrow">AI APPLICATIONS LAB</div><h1>Student Lab Access</h1><p>Enter the class access code to open the {APP_TITLE}.</p></div>', unsafe_allow_html=True)
            entered = st.text_input("Class access code", type="password", placeholder="Enter the code provided in class")
            if st.button("Enter Application", type="primary", use_container_width=True):
                if expected and hmac.compare_digest(entered, expected):
                    st.session_state["class_access_granted"] = True; st.rerun()
                st.error("Incorrect class code. Please try again.")
            if not expected: st.warning("Class access has not been configured by the application owner.")
            st.markdown('<div class="access-note">Access is restricted to classroom participants.</div>', unsafe_allow_html=True)
    st.stop()

def header():
    title, controls = st.columns([5, 2])
    with title: st.markdown(f'<div class="hero"><div class="eyebrow">{APP_AREA}</div><h1>{APP_TITLE}</h1><p>{APP_SUBTITLE}</p></div>', unsafe_allow_html=True)
    with controls:
        st.link_button("← Back to AI Applications Lab", "https://aiapplicationslab.in", use_container_width=True)
        if st.button("Exit Lab", use_container_width=True): st.session_state["class_access_granted"] = False; st.rerun()
    st.markdown('<div class="notice"><strong>Educational AI classroom prototype:</strong> Use this application to explore model behaviour and product decisions. Its estimates show associations in teaching data and should not be treated as causal evidence.</div>', unsafe_allow_html=True)

require_access(); header()

left, right = st.columns([5, 8], gap="large")
with left:
    with st.container(border=True):
        st.markdown('<div class="section-title">Product inputs</div><div class="section-copy">Adjust the early-experience indicators to create a retention scenario.</div>', unsafe_allow_html=True)
        onboarding = st.slider("Onboarding completion (%)", 0.0, 100.0, 65.0, 1.0)
        push_opt_in = st.slider("Push opt-in (%)", 0.0, 100.0, 45.0, 1.0)
        sessions = st.slider("Average sessions in Week 1", 0.0, 20.0, 4.0, 0.1)

predicted = COEFFICIENTS["Intercept"] + COEFFICIENTS["Onboarding completion"]*onboarding + COEFFICIENTS["Push opt-in"]*push_opt_in + COEFFICIENTS["Week 1 sessions"]*sessions
predicted = max(0.0, min(100.0, predicted))
rows = [("Onboarding completion",onboarding,COEFFICIENTS["Onboarding completion"],onboarding*COEFFICIENTS["Onboarding completion"]),("Push opt-in",push_opt_in,COEFFICIENTS["Push opt-in"],push_opt_in*COEFFICIENTS["Push opt-in"]),("Week 1 sessions",sessions,COEFFICIENTS["Week 1 sessions"],sessions*COEFFICIENTS["Week 1 sessions"])]

with right:
    with st.container(border=True):
        st.markdown('<div class="section-title">AI model insight</div><div class="section-copy">Review the prediction, its drivers and a counterfactual product scenario.</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="result-card"><div class="result-label">Predicted D7 retention</div><div class="result-value">{predicted:.1f}%</div><div>Estimated from the current combination of product-experience inputs.</div></div>', unsafe_allow_html=True)
        st.subheader("What is driving the prediction?")
        st.dataframe({"Driver":[r[0] for r in rows],"Current value":[r[1] for r in rows],"Model coefficient":[r[2] for r in rows],"Contribution (percentage points)":[round(r[3],2) for r in rows]},hide_index=True,use_container_width=True)
        st.subheader("Scenario comparison")
        lever = st.selectbox("Choose a lever", ["Onboarding completion","Push opt-in","Week 1 sessions"])
        change = st.slider("Improvement",0.0,20.0 if lever!="Week 1 sessions" else 5.0,5.0 if lever!="Week 1 sessions" else 1.0,0.5)
        scenario_lift = COEFFICIENTS[lever]*change
        st.info(f"A {change:g}-unit improvement in **{lever}** is associated with an estimated **{scenario_lift:.2f} percentage-point** change in D7 retention.")

with st.expander("Model logic and classroom interpretation"):
    st.markdown("""**Model equation**

`D7 Retention (%) = 0.1941 + 0.0466 × Onboarding Completion + 0.0604 × Push Opt-in + 0.1931 × Avg. Sessions in Week 1`

The estimates describe association in the original cohort data. Use them to form hypotheses and validate those hypotheses through product experiments.""")
st.markdown('<div class="footer">AI Applications Lab · Analytical AI · Guided classroom learning</div>', unsafe_allow_html=True)

