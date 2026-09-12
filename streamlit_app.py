import streamlit as st

st.set_page_config(page_title="D7 Retention Explorer", page_icon="📈", layout="wide")

COEFFICIENTS = {
    "Intercept": 0.1941,
    "Onboarding completion": 0.0466,
    "Push opt-in": 0.0604,
    "Week 1 sessions": 0.1931,
}

def require_class_code() -> None:
    if st.session_state.get("class_access_granted"):
        return

    expected_code = st.secrets.get("STUDENT_ACCESS_CODE", "")
    st.title("D7 Retention Explorer")
    st.caption("Classroom access")

    if not expected_code:
        st.error("Class-code access has not been configured for this app.")
        st.stop()

    with st.form("class_code_form"):
        code = st.text_input("Class code", type="password", placeholder="Enter code")
        submitted = st.form_submit_button("Open explorer", use_container_width=True)

    if submitted:
        if code.strip().casefold() == expected_code.strip().casefold():
            st.session_state.class_access_granted = True
            st.rerun()
        st.error("That class code is not valid. Please check it and try again.")
    st.stop()


require_class_code()

st.title("D7 Retention Explorer")
st.caption("Use a multiple linear regression model to explore how early product experience indicators relate to seven-day retention.")

with st.sidebar:
    st.header("Product inputs")
    onboarding = st.slider("Onboarding completion (%)", 0.0, 100.0, 65.0, 1.0)
    push_opt_in = st.slider("Push opt-in (%)", 0.0, 100.0, 45.0, 1.0)
    sessions = st.slider("Average sessions in Week 1", 0.0, 20.0, 4.0, 0.1)

predicted = (
    COEFFICIENTS["Intercept"]
    + COEFFICIENTS["Onboarding completion"] * onboarding
    + COEFFICIENTS["Push opt-in"] * push_opt_in
    + COEFFICIENTS["Week 1 sessions"] * sessions
)
predicted = max(0.0, min(100.0, predicted))

st.metric("Predicted D7 retention", f"{predicted:.1f}%")

st.subheader("What is driving the prediction?")
rows = [
    ("Onboarding completion", onboarding, COEFFICIENTS["Onboarding completion"], onboarding * COEFFICIENTS["Onboarding completion"]),
    ("Push opt-in", push_opt_in, COEFFICIENTS["Push opt-in"], push_opt_in * COEFFICIENTS["Push opt-in"]),
    ("Week 1 sessions", sessions, COEFFICIENTS["Week 1 sessions"], sessions * COEFFICIENTS["Week 1 sessions"]),
]
st.dataframe(
    {
        "Driver": [row[0] for row in rows],
        "Current value": [row[1] for row in rows],
        "Model coefficient": [row[2] for row in rows],
        "Contribution (percentage points)": [round(row[3], 2) for row in rows],
    },
    hide_index=True,
    use_container_width=True,
)

st.subheader("Scenario comparison")
st.write("Change one product lever to see its estimated association with D7 retention, holding the other inputs constant.")
lever = st.selectbox("Choose a lever", ["Onboarding completion", "Push opt-in", "Week 1 sessions"])
change = st.slider("Improvement", 0.0, 20.0 if lever != "Week 1 sessions" else 5.0, 5.0 if lever != "Week 1 sessions" else 1.0, 0.5)
scenario_lift = COEFFICIENTS[lever] * change
st.info(f"A {change:g}-unit improvement in **{lever}** is associated with an estimated **{scenario_lift:.2f} percentage-point** change in D7 retention.")

with st.expander("Model notes and classroom interpretation"):
    st.markdown("""
**Model equation**

`D7 Retention (%) = 0.1941 + 0.0466 × Onboarding Completion + 0.0604 × Push Opt-in + 0.1931 × Avg. Sessions in Week 1`

The estimates describe association in the original cohort data. They do not, by themselves, establish that changing a lever will cause retention to change. Use the results to form hypotheses, then validate them through product experiments.
""")
