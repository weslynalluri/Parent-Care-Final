# import streamlit as st
# from utils import get_model_info

# st.set_page_config(
#     page_title="ParentCare — Child Digital Wellness",
#     page_icon="🧒",
#     layout="wide",
#     initial_sidebar_state="expanded"
# )

# # ── Real model info from API ──────────────────────────────
# @st.cache_data(ttl=3600)
# def load_model_info():
#     try:
#         return get_model_info()
#     except Exception:
#         return {"algorithm": "Random Forest", "accuracy": "—",
#                 "total_records": "9,668", "features_used": 7}

# info = load_model_info()

# # ── Page ──────────────────────────────────────────────────
# st.title("🧒 ParentCare")
# st.subheader("Child Digital Wellness Assessment Platform")
# st.markdown("Helping Indian parents understand and improve their child's digital health using Machine Learning.")
# st.divider()

# # ── Stats — all from real data, no hardcoding ─────────────
# c1, c2, c3, c4 = st.columns(4)
# c1.metric("Children in Dataset",  f"{info.get('total_records', 9668):,}")
# c2.metric("Model Accuracy",       f"{info.get('accuracy', '—')}%")
# c3.metric("Algorithm",            info.get('algorithm', 'Random Forest'))
# c4.metric("Features Used",        info.get('features_used', 7))

# st.divider()

# # ── What the platform does ────────────────────────────────
# st.subheader("What ParentCare does for you")

# col1, col2 = st.columns(2)
# with col1:
#     st.info("**📊 Wellness Assessment**\nEnter your child's screen habits and get a 0–100 wellness score with category.")
#     st.info("**⚠️ Screen Time Alerts**\nGet a clear alert if your child's screen time exceeds the safe daily limit.")
#     st.info("**💡 Health Recommendations**\nPractical, simple tips for sleep, eye care, anxiety, and activity levels.")

# with col2:
#     st.info("**🤖 ML Prediction**\nRandom Forest model trained on 9,668 Indian children predicts wellness category.")
#     st.info("**🎯 Age-Appropriate Activities**\nOffline activity suggestions matched to your child's age group.")
#     st.info("**🥗 Diet Tips**\nSimple food advice based on your child's specific health concerns.")

# st.divider()

# # ── Simple steps ──────────────────────────────────────────
# st.subheader("How to use ParentCare")
# s1, s2, s3 = st.columns(3)
# s1.success("**Step 1**\n\nGo to **Child Assessment** in the sidebar and fill in your child's details.")
# s2.success("**Step 2**\n\nClick **Assess My Child** — the system analyses screen habits and health signals.")
# s3.success("**Step 3**\n\nRead the wellness report with score, alert, recommendations, activities and diet tips.")

# st.divider()
# st.caption("Built with FastAPI · scikit-learn · Pandas · Streamlit · Plotly")
# st.info("👈 Use the sidebar to navigate to **Child Assessment** or **Analytics Dashboard**")


import streamlit as st

st.set_page_config(
    page_title="ParentCare",
    page_icon="🧒",
    layout="wide"
)

st.title("🧒 ParentCare")
st.subheader("AI-Powered Child Digital Wellness Assessment")

st.write("""
ParentCare helps parents understand their child's digital wellness by
analyzing daily screen habits and providing simple, personalized
recommendations to encourage healthier digital lifestyles.
""")

st.divider()

st.header("🎯 Why Choose ParentCare?")

col1, col2 = st.columns(2)

with col1:
    st.success("✔ Monitor your child's digital wellness")
    st.success("✔ Identify possible health risks")
    st.success("✔ Improve healthy screen habits")

with col2:
    st.success("✔ Receive personalized recommendations")
    st.success("✔ Discover age-appropriate activities")
    st.success("✔ Support balanced digital usage")

st.divider()

st.header("⚙️ How It Works")

step1, step2, step3, step4 = st.columns(4)

with step1:
    st.info("""
    **Step 1**

    Enter your child's information.
    """)

with step2:
    st.info("""
    **Step 2**

    ParentCare analyzes digital wellness.
    """)

with step3:
    st.info("""
    **Step 3**

    View the wellness assessment report.
    """)

with step4:
    st.info("""
    **Step 4**

    Follow personalized recommendations and activities.
    """)

st.divider()

st.header("✨ What You'll Receive")

feature1, feature2 = st.columns(2)

with feature1:
    st.markdown("""
- 📱 Screen Time Analysis
- 🩺 Health Risk Assessment
- ❤️ Wellness Score
- ⚠️ Screen Time Alerts
""")

with feature2:
    st.markdown("""
- 💡 Personalized Recommendations
- 🎯 Suggested Activities
- 📊 Wellness Dashboard
- 👨‍👩‍👧 Easy-to-understand Reports
""")

st.divider()

st.info("👈 Use the sidebar to open **Child Assessment** and begin your child's wellness assessment.")