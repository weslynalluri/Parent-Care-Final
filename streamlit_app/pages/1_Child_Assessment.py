import streamlit as st
import plotly.graph_objects as go
from utils import assess_child

st.set_page_config(page_title="Assessment — ParentCare", page_icon="📝", layout="wide")

st.title("📝 Child Wellness Assessment")
st.caption("Fill in the details below and click Assess My Child.")
st.divider()

# ── FORM ─────────────────────────────────────────────────
with st.form("form"):
    col1, col2 = st.columns(2)

    with col1:
        name        = st.text_input("Child's Name", placeholder="e.g. Arjun")
        age         = st.number_input("Age", min_value=8, max_value=18, value=12)
        gender      = st.selectbox("Gender", ["Male", "Female"])
        location    = st.radio("Area", ["Urban", "Rural"], horizontal=True)

    with col2:
        device      = st.selectbox("Primary Device", ["Smartphone", "Laptop", "TV", "Tablet"])
        screen_time = st.slider("Daily Screen Time (hours)", 0, 16, 4)
        edu_pct     = st.slider("Educational Screen Use (%)", 0, 100, 40,
                                help="What % of screen time is for study or learning?")

    st.divider()
    st.subheader("Current Health Concerns")
    st.caption("Tick any that apply to your child right now:")
    h1, h2 = st.columns(2)
    with h1:
        poor_sleep   = st.checkbox("😴 Poor Sleep")
        eye_strain   = st.checkbox("👁️ Eye Strain")
    with h2:
        anxiety      = st.checkbox("😰 Anxiety or Stress")
        obesity_risk = st.checkbox("⚖️ Low Physical Activity / Weight Concern")

    go_btn = st.form_submit_button("🔍 Assess My Child", use_container_width=True, type="primary")

# ── CALL API ─────────────────────────────────────────────
if go_btn:
    payload = {
        "age": int(age), "screen_time": float(screen_time),
        "educational_ratio": edu_pct / 100,
        "poor_sleep": poor_sleep, "eye_strain": eye_strain,
        "anxiety": anxiety, "obesity_risk": obesity_risk,
        "gender": gender, "urban_or_rural": location,
    }
    try:
        with st.spinner("Analysing..."):
            result = assess_child(payload)
        st.session_state["result"] = result
        st.session_state["child"]  = {
            "name": name or "Your Child", "age": age, "gender": gender,
            "device": device, "location": location, "screen_time": screen_time,
            "edu_pct": edu_pct, "poor_sleep": poor_sleep, "eye_strain": eye_strain,
            "anxiety": anxiety, "obesity_risk": obesity_risk,
        }
    except Exception as e:
        st.error(f"Could not reach the API. Make sure FastAPI is running.\n\nError: {e}")
        st.stop()

if "result" not in st.session_state:
    st.stop()

r     = st.session_state["result"]
child = st.session_state["child"]
alert = r["screen_time_alert"]

st.divider()

# ── CHILD HEADER ─────────────────────────────────────────
cat_color = {"Healthy":"#2e7d32","Moderate":"#f57f17",
             "High Risk":"#e65100","Critical":"#b71c1c"}.get(r["wellness_category"],"#555")

st.markdown(f"""
<div style="background:linear-gradient(135deg,#667eea,#764ba2);padding:1.2rem 1.8rem;
            border-radius:12px;color:white;margin-bottom:1rem">
    <div style="font-size:1.5rem;font-weight:700">🧒 {child['name']}</div>
    <div style="font-size:0.88rem;opacity:0.85;margin-top:0.3rem">
        Age {child['age']} &nbsp;|&nbsp; {child['gender']} &nbsp;|&nbsp;
        {child['device']} &nbsp;|&nbsp; {child['location']} &nbsp;|&nbsp;
        {child['screen_time']} hrs/day &nbsp;|&nbsp; {child['edu_pct']}% educational
    </div>
</div>""", unsafe_allow_html=True)

# ── WELLNESS SCORE ────────────────────────────────────────
st.subheader("Wellness Score")
g_col, m_col = st.columns([1,1])

with g_col:
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=r["wellness_score"],
        title={"text":"Score (0–100)","font":{"size":14}},
        gauge={"axis":{"range":[0,100]}, "bar":{"color":cat_color},
               "steps":[{"range":[0,40],"color":"#ffcdd2"},{"range":[40,60],"color":"#ffe0b2"},
                        {"range":[60,80],"color":"#fff9c4"},{"range":[80,100],"color":"#c8e6c9"}]}
    ))
    fig.update_layout(height=230, margin=dict(t=40,b=10,l=20,r=20))
    st.plotly_chart(fig, use_container_width=True)

with m_col:
    st.markdown("<br>", unsafe_allow_html=True)
    ma, mb = st.columns(2)
    ma.metric("Category",     r["wellness_category"])
    mb.metric("ML Prediction",r["ml_prediction"])
    mc, md = st.columns(2)
    mc.metric("Confidence",   f"{r['ml_confidence']}%")
    md.metric("Concern Count",f"{r['concern_count']} / 4")

# ── SCREEN TIME ALERT ─────────────────────────────────────
st.subheader("⏱️ Screen Time Alert")
lvl = alert["alert_level"]
msg = alert["message"]
if lvl == "safe":
    st.success(f"✅ {msg}")
elif lvl == "warning":
    c1,c2 = st.columns([3,1]); c1.warning(f"⚠️ {msg}"); c2.metric("Over limit",f"{alert['excess_hours']} hrs")
elif lvl == "alert":
    c1,c2 = st.columns([3,1]); c1.error(f"🚨 {msg}"); c2.metric("Over limit",f"{alert['excess_hours']} hrs")
else:
    c1,c2 = st.columns([3,1]); c1.error(f"🔴 {msg}"); c2.metric("Over limit",f"{alert['excess_hours']} hrs")

# ── HEALTH INDICATORS ─────────────────────────────────────
st.subheader("🩺 Health Indicators")
hcols = st.columns(4)
for col,(label,val) in zip(hcols,[
    ("😴 Poor Sleep",   child["poor_sleep"]),
    ("👁️ Eye Strain",   child["eye_strain"]),
    ("😰 Anxiety",      child["anxiety"]),
    ("⚖️ Low Activity", child["obesity_risk"]),
]):
    if val: col.error(f"**{label}**\n\n✔ Present")
    else:   col.success(f"**{label}**\n\n✖ Not reported")

st.divider()

# ── RECOMMENDATIONS ───────────────────────────────────────
st.subheader("💡 Recommendations")
for i, rec in enumerate(r["recommendations"], 1):
    st.markdown(f"""
    <div style="background:#1e293b;padding:14px 16px;border-radius:10px;
                margin-bottom:10px;border-left:5px solid #4ade80;color:white;font-size:0.9rem">
        <strong>#{i}</strong> &nbsp; {rec}
    </div>""", unsafe_allow_html=True)

# ── DIET TIPS ─────────────────────────────────────────────
if r["diet_tips"]:
    st.subheader("🥗 Diet Tips")
    d1, d2 = st.columns(2)
    for i, tip in enumerate(r["diet_tips"]):
        (d1 if i % 2 == 0 else d2).info(tip)

# ── ACTIVITIES ────────────────────────────────────────────
st.subheader("🎯 Suggested Activities")
st.caption(f"Age-appropriate offline activities for {child['age']}-year-olds")
acts = r["activity_suggestions"]
if acts and "🔴" in acts[0]:
    st.warning(acts[0]); acts = acts[1:]
a1, a2 = st.columns(2)
for i, act in enumerate(acts):
    (a1 if i % 2 == 0 else a2).success(act)

st.divider()
st.caption("ParentCare Analytics v2.0 | AI-Powered Child Digital Wellness Platform")


# if st.button("👨‍👩‍👧 View Parent Guidance"):
#     st.switch_page("pages/3_Parent_Guidance.py")