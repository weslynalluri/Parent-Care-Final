"""
Simple, parent-friendly recommendations.
Only shows what parents actually need to know.
"""

# ── Health Recommendations ────────────────────────────────
def generate_recommendations(
    wellness_category,
    poor_sleep,
    eye_strain,
    anxiety,
    obesity_risk,
    educational_ratio=0.5,
    urban_or_rural="Urban"
):
    recs = []

    # Overall wellness
    if wellness_category == "Critical":
        recs.append("🚨 Your child's digital wellness needs immediate attention. Reduce recreational screen time immediately and closely monitor daily habits.")
    elif wellness_category == "High Risk":
        recs.append("⚠️ Reduce recreational screen time by at least 1–2 hours every day.")
    elif wellness_category == "Moderate":
        recs.append("📋 Small improvements in daily routines can greatly improve your child's digital wellness.")
    else:
        recs.append("✅ Your child currently has healthy digital habits. Continue maintaining a balanced routine.")

    # Health recommendations
    if poor_sleep:
        recs.append("😴 Avoid screens for at least one hour before bedtime and keep devices outside the bedroom.")

    if eye_strain:
        recs.append("👁️ Follow the 20-20-20 rule and ensure proper room lighting while using digital devices.")

    if anxiety:
        recs.append("🧘 Encourage daily conversations, outdoor play, and reduce unnecessary social media exposure.")

    if obesity_risk:
        recs.append("🏃 Encourage at least 60 minutes of physical activity every day.")

    if educational_ratio < 0.30:
        recs.append("📚 Increase educational screen activities such as learning apps or educational videos.")

    # Location-specific recommendations
    if urban_or_rural == "Urban":

        recs.append("🌳 Visit nearby parks or playgrounds regularly instead of spending weekends indoors.")
        recs.append("🚲 Encourage cycling, skating, swimming, or organized sports available in your city.")
        recs.append("📖 Visit local libraries, museums, or children's learning centres whenever possible.")

    else:

        recs.append("🌾 Encourage outdoor activities such as farming support, gardening, or nature walks.")
        recs.append("⚽ Promote traditional village games like Kabaddi, Kho-Kho, Gilli Danda, or Cricket.")
        recs.append("👨‍👩‍👧 Encourage participation in community events and cultural activities.")

    return recs


# ── Activity Suggestions by Age ───────────────────────────
URBAN_ACTIVITIES = {

    "8-10": [
        "🎨 Drawing or colouring",
        "🚴 Cycling",
        "📖 Story books",
        "⚽ Cricket in the park",
        "🧩 Puzzle games",
        "♟ Chess"
    ],

    "11-13": [
        "🏸 Badminton",
        "⚽ Football",
        "🎵 Music classes",
        "🔬 Science experiments",
        "💻 Scratch programming",
        "📚 Reading books"
    ],

    "14-16": [
        "💻 Learn Python",
        "📷 Photography",
        "🎸 Learn guitar",
        "🏃 Gym or jogging",
        "🎭 Debate club",
        "📚 Career books"
    ],

    "17-18": [
        "💻 Build projects",
        "🏋 Gym",
        "📚 Self-development books",
        "🎵 Music production",
        "🌍 Learn languages",
        "🤝 Volunteering"
    ]

}

RURAL_ACTIVITIES = {

    "8-10": [
        "🌳 Nature walk",
        "⚽ Cricket",
        "🏃 Running",
        "🎨 Drawing",
        "📖 Story books",
        "🌱 Gardening"
    ],

    "11-13": [
        "🏏 Cricket",
        "🤸 Kabaddi",
        "🏃 Kho-Kho",
        "🌾 Gardening",
        "📖 Library reading",
        "🚴 Cycling"
    ],

    "14-16": [
        "🌱 Organic gardening",
        "🏏 Village sports",
        "🔧 DIY craft work",
        "📚 Competitive exam reading",
        "🏃 Athletics",
        "🎭 Cultural programs"
    ],

    "17-18": [
        "🚜 Agricultural innovation projects",
        "🏏 Sports tournaments",
        "📚 Skill development",
        "🔧 Mechanical hobby projects",
        "🤝 Community volunteering",
        "💡 Entrepreneurship ideas"
    ]

}


def generate_activity_suggestions(
    age_group,
    wellness_category,
    urban_or_rural="Urban"
):

    if urban_or_rural == "Urban":
        activities = list(
            URBAN_ACTIVITIES.get(age_group, URBAN_ACTIVITIES["11-13"])
        )
    else:
        activities = list(
            RURAL_ACTIVITIES.get(age_group, RURAL_ACTIVITIES["11-13"])
        )

    if wellness_category in ("Critical", "High Risk"):
        activities.insert(
            0,
            "🔴 Reduce one hour of screen time daily by replacing it with any activity below."
        )

    return activities[:6]


# ── Diet Tips by Health Condition ─────────────────────────
def generate_diet_tips(
    poor_sleep,
    eye_strain,
    anxiety,
    obesity_risk,
    urban_or_rural="Urban"
):
    tips = []
    if poor_sleep:
        tips.append("🥛 Give warm milk before bedtime — it contains tryptophan which helps sleep.")
        tips.append("🍌 Banana at dinner helps — rich in magnesium which relaxes muscles.")
        tips.append("🚫 Avoid tea, coffee, or cold drinks after 4 PM.")
    if eye_strain:
        tips.append("🥕 Include carrots and spinach daily — Vitamin A and lutein protect eyesight.")
        tips.append("🍊 Give citrus fruits — Vitamin C supports eye health.")
        tips.append("🐟 Fish or flaxseed oil 2–3 times a week for omega-3.")
    if anxiety:
        tips.append("🥜 Handful of nuts and seeds daily — magnesium reduces anxiety.")
        tips.append("🍫 Small piece of dark chocolate is okay — helps mood naturally.")
        tips.append("🚫 Avoid sugary snacks and energy drinks — they worsen anxiety.")
    if obesity_risk:
        tips.append("💧 2 litres of water daily — before meals to reduce overeating.")
        tips.append("🥦 Fill half the plate with vegetables at every meal.")
        tips.append("🚫 No fried snacks or packaged biscuits — swap with fruit or roasted chana.")
    if not tips:
        tips.append("🍎 Continue a balanced diet — include fruits, vegetables, protein, and plenty of water daily.")
    
    return tips



