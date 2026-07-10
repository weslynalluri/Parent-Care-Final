from pydantic import BaseModel, Field
from typing import Optional


class ChildAssessmentRequest(BaseModel):
    age: int = Field(..., ge=8, le=18)
    screen_time: float = Field(..., ge=0, le=16)
    educational_ratio: float = Field(default=0.5, ge=0.0, le=1.0)
    poor_sleep: bool
    eye_strain: bool
    anxiety: bool
    obesity_risk: bool
    gender: Optional[str] = "Male"
    urban_or_rural: Optional[str] = "Urban"

    class Config:
        json_schema_extra = {"example": {
            "age": 12, "screen_time": 5.0, "educational_ratio": 0.35,
            "poor_sleep": True, "eye_strain": True, "anxiety": False,
            "obesity_risk": False, "gender": "Male", "urban_or_rural": "Urban"
        }}


class AssessmentResponse(BaseModel):
    age_group: str
    screen_risk: str
    risk_points: int
    health_penalty: int
    wellness_score: int
    wellness_category: str
    priority_level: str
    concern_count: int
    intervention_level: str
    educational_ratio_flag: str
    ml_prediction: str
    ml_confidence: float
    probabilities: dict
    screen_time_alert: dict
    recommendations: list[str]
    activity_suggestions: list[str]
    diet_tips: list[str]
