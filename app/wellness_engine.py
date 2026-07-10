def get_age_group(age: int) -> str:
    if 8 <= age <= 10:    return "8-10"
    elif 11 <= age <= 13: return "11-13"
    elif 14 <= age <= 16: return "14-16"
    elif 17 <= age <= 18: return "17-18"
    raise ValueError(f"Age {age} must be between 8 and 18.")


def get_screen_risk(screen_time: float) -> str:
    if screen_time < 2:   return "Low Risk"
    elif screen_time < 4: return "Moderate Risk"
    return "High Risk"


def get_risk_points(screen_risk: str) -> int:
    return {"Low Risk": 100, "Moderate Risk": 70, "High Risk": 40}.get(screen_risk, 40)


def calculate_health_penalty(poor_sleep, eye_strain, anxiety, obesity_risk) -> int:
    return (15 if poor_sleep else 0) + (10 if eye_strain else 0) + \
           (10 if anxiety else 0)    + (5  if obesity_risk else 0)


def get_educational_ratio_flag(ratio: float) -> str:
    if ratio >= 0.6:   return "Educationally Balanced"
    elif ratio >= 0.4: return "Moderate Recreational Use"
    return "High Recreational Use"


def get_wellness_category(score: int) -> str:
    if score >= 80: return "Healthy"
    elif score >= 60: return "Moderate"
    elif score >= 40: return "High Risk"
    return "Critical"


def get_priority_level(category: str) -> str:
    return {"Critical": "Critical", "High Risk": "High",
            "Moderate": "Medium", "Healthy": "Low"}.get(category, "Low")


def get_concern_count(poor_sleep, eye_strain, anxiety, obesity_risk) -> int:
    return sum([poor_sleep, eye_strain, anxiety, obesity_risk])


def get_intervention_level(count: int) -> str:
    if count >= 3: return "Immediate Attention"
    elif count == 2: return "Monitor Closely"
    elif count == 1: return "Preventive Action"
    return "Healthy Monitoring"


def build_screen_time_alert(screen_time: float) -> dict:
    limit   = 2.0
    exceeded = screen_time > limit
    excess   = round(max(0.0, screen_time - limit), 2)
    if not exceeded:
        level, msg = "safe", f"Screen time ({screen_time} hrs) is within the safe limit of 2 hrs/day."
    elif excess <= 1.0:
        level, msg = "warning", f"Screen time is {excess} hrs above the recommended limit. Consider a schedule."
    elif excess <= 3.0:
        level, msg = "alert", f"Screen time is {excess} hrs above the limit. Parental controls advised."
    else:
        level, msg = "critical", f"Screen time is critically high — {excess} hrs above daily recommendation."
    return {"exceeded_limit": exceeded, "daily_screen_time": screen_time,
            "recommended_limit_hrs": limit, "excess_hours": excess,
            "alert_level": level, "message": msg}


def assess_child(age, screen_time, poor_sleep, eye_strain,
                 anxiety, obesity_risk, educational_ratio=0.5) -> dict:
    age_group      = get_age_group(age)
    screen_risk    = get_screen_risk(screen_time)
    risk_points    = get_risk_points(screen_risk)
    health_penalty = calculate_health_penalty(poor_sleep, eye_strain, anxiety, obesity_risk)
    edu_flag       = get_educational_ratio_flag(educational_ratio)

    if educational_ratio < 0.3:
        health_penalty = min(health_penalty + 5, 40)

    wellness_score    = max(0, risk_points - health_penalty)
    wellness_category = get_wellness_category(wellness_score)
    priority_level    = get_priority_level(wellness_category)
    concern_count     = get_concern_count(poor_sleep, eye_strain, anxiety, obesity_risk)
    intervention      = get_intervention_level(concern_count)
    screen_alert      = build_screen_time_alert(screen_time)

    return {
        "age_group": age_group, "screen_risk": screen_risk,
        "risk_points": risk_points, "health_penalty": health_penalty,
        "wellness_score": wellness_score, "wellness_category": wellness_category,
        "priority_level": priority_level, "concern_count": concern_count,
        "intervention_level": intervention, "educational_ratio_flag": edu_flag,
        "screen_time_alert": screen_alert,
    }
