import streamlit as st
import random

st.set_page_config(
    page_title="Parent Guide",
    page_icon="👨‍👩‍👧",
    layout="wide"
)

st.title("👨‍👩‍👧 Parent Guide")
st.write(
    """
ParentCare helps you understand your child's digital habits and supports you
with simple suggestions to build a healthier daily routine.

Healthy digital habits begin at home. Small changes made by parents can make
a big difference in a child's life.
"""
)

st.divider()

# ----------------------------------------------------
# Parent Self Check
# ----------------------------------------------------

st.header("🌟 Parent Self Check")

st.write("Tick the habits that match your daily routine.")

q1 = st.checkbox("📱 I use my phone during family meals.")
q2 = st.checkbox("📱 I often check my phone while talking with my child.")
q3 = st.checkbox("🌙 I use my phone before sleeping.")
q4 = st.checkbox("⏰ I spend more than 3 hours on my phone every day.")
q5 = st.checkbox("🏃 I rarely spend outdoor time with my child.")

score = 100

for item in [q1, q2, q3, q4, q5]:
    if item:
        score -= 20

st.metric("Parent Healthy Habit Score", f"{score}/100")

if score >= 80:
    st.success("Great! You are setting a good example for your child.")
elif score >= 60:
    st.warning("Good start. A few small changes can help your child develop healthier habits.")
else:
    st.error("Your daily habits may also influence your child's digital behaviour. Try making one small change every week.")

st.divider()

# ----------------------------------------------------
# Suggestions
# ----------------------------------------------------

st.header("💡 Suggestions for Parents")

tips = []

if q1:
    tips.append("🍽 Keep phones away during family meals.")

if q2:
    tips.append("👂 Give your full attention when your child is talking.")

if q3:
    tips.append("🌙 Avoid using your phone for at least 30 minutes before bedtime.")

if q4:
    tips.append("📵 Reduce your own screen time little by little each day.")

if q5:
    tips.append("⚽ Spend at least 30 minutes outdoors with your child every day.")

if not tips:
    st.success("You are already following many healthy habits. Keep encouraging your child.")

for tip in tips:
    st.info(tip)

st.divider()

# ----------------------------------------------------
# Family Activities
# ----------------------------------------------------

st.header("🏡 Healthy Family Ideas")

st.success("✔ Eat one meal together without mobile phones.")
st.success("✔ Spend at least 30 minutes talking with your child every day.")
st.success("✔ Read a book or story together.")
st.success("✔ Play an outdoor game every weekend.")
st.success("✔ Encourage hobbies like drawing, music, sports or gardening.")
st.success("✔ Keep mobile phones out of the bedroom during sleep.")

st.divider()

# ----------------------------------------------------
# Today's Tip
# ----------------------------------------------------

st.header("💬 Today's Parenting Tip")

daily_tips = [

    "Children learn more from what parents do than what parents say.",

    "Spend a few minutes talking with your child without using any devices.",

    "Outdoor play helps improve physical and mental health.",

    "Reading together helps build stronger family relationships.",

    "Keep meal time free from mobile phones and television.",

    "Praise your child for healthy habits instead of only pointing out mistakes.",

    "Set simple screen time rules and follow them together as a family.",

    "Be a role model by limiting your own screen time."

]

st.info(random.choice(daily_tips))

st.divider()

# ----------------------------------------------------
# Family Promise
# ----------------------------------------------------

st.header("🤝 Family Promise")

st.checkbox("We will eat meals without using mobile phones.")
st.checkbox("We will spend quality time together every day.")
st.checkbox("We will encourage outdoor games and physical activity.")
st.checkbox("We will follow healthy screen time habits together.")

st.success("Healthy children grow in healthy families. Every small step counts.")

st.divider()

st.caption(
    "ParentCare provides guidance to support healthy digital habits. "
    "It does not replace professional medical advice."
)