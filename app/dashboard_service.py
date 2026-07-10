import pandas as pd
from pathlib import Path
import logging

logger = logging.getLogger(__name__)

_PATH = Path(__file__).resolve().parent.parent / "data" / "ParentCare_Final_Dataset.csv"

try:
    _df = pd.read_csv(_PATH)
    logger.info(f"Dataset loaded: {len(_df)} records")
except Exception as e:
    raise RuntimeError(f"Dataset not found at {_PATH}. Copy ParentCare_Final_Dataset.csv to data/")


def get_dashboard_summary() -> dict:
    return {
        "total_children":         len(_df),
        "average_screen_time":    round(_df["Avg_Daily_Screen_Time_hr"].mean(), 2),
        "high_risk_pct":          round((_df["Screen_Risk"] == "High Risk").mean() * 100, 1),
        "avg_wellness_score":     round(_df["Digital_Wellness_Score"].mean(), 1),
        "critical_cases":         int((_df["Wellness_Category"] == "Critical").sum()),
        "healthy_cases":          int((_df["Wellness_Category"] == "Healthy").sum()),
    }


def get_wellness_distribution() -> dict:
    return _df["Wellness_Category"].value_counts().to_dict()


def get_age_group_analysis() -> list[dict]:
    result = (
        _df.groupby("Age_Group")
        .agg(avg_screen_time=("Avg_Daily_Screen_Time_hr","mean"),
             avg_wellness_score=("Digital_Wellness_Score","mean"),
             total=("Age","count"))
        .round(2).reset_index()
    )
    return result.to_dict(orient="records")


def get_health_concerns() -> dict:
    return {
        "Poor Sleep":   int(_df["Poor_Sleep"].sum()),
        "Eye Strain":   int(_df["Eye_Strain"].sum()),
        "Anxiety":      int(_df["Anxiety"].sum()),
        "Obesity Risk": int(_df["Obesity_Risk"].sum()),
    }


def get_device_analysis() -> list[dict]:
    result = (
        _df.groupby("Primary_Device")
        .agg(total=("Age","count"),
             avg_screen_time=("Avg_Daily_Screen_Time_hr","mean"))
        .round(2).reset_index()
        .sort_values("avg_screen_time", ascending=False)
    )
    return result.to_dict(orient="records")


def get_urban_rural() -> list[dict]:
    result = (
        _df.groupby("Urban_or_Rural")
        .agg(total=("Age","count"),
             avg_screen_time=("Avg_Daily_Screen_Time_hr","mean"),
             avg_wellness_score=("Digital_Wellness_Score","mean"))
        .round(2).reset_index()
    )
    return result.to_dict(orient="records")
