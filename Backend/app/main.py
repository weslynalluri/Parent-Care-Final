import logging
from fastapi import FastAPI, HTTPException, Depends, Request
from fastapi.middleware.cors import CORSMiddleware
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded

from app.models import ChildAssessmentRequest, AssessmentResponse
from app.wellness_engine import assess_child
from app.ml_engine import predict_wellness, get_model_metadata
from app.recommendation_engine import (
    generate_recommendations,
    generate_activity_suggestions,
    generate_diet_tips,
)
from app.dashboard_service import (
    get_dashboard_summary, get_wellness_distribution,
    get_age_group_analysis, get_health_concerns,
    get_device_analysis, get_urban_rural,
)
from app.security import verify_api_key

logging.basicConfig(level=logging.INFO, format="%(asctime)s | %(levelname)s | %(message)s")
logger = logging.getLogger(__name__)

limiter = Limiter(key_func=get_remote_address, default_limits=["60/minute"])

app = FastAPI(
    title="ParentCare Analytics API",
    description="""
## ParentCare — Child Digital Wellness Assessment

A data-driven API to help Indian parents understand their child's digital wellness.

**What it does:**
- Assesses digital wellness from screen habits and health indicators
- Predicts wellness category using a trained Random Forest model
- Provides actionable recommendations, diet tips, and age-appropriate activities
- Delivers population-level analytics from 9,668 child records

**Assessment endpoints** require an `X-API-Key` header.  
**Analytics endpoints** are public.
""",
    version="2.0.0",
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(CORSMiddleware, allow_origins=["*"],
                   allow_credentials=True, allow_methods=["*"], allow_headers=["*"])


# ── System ────────────────────────────────────────────────

@app.get("/", tags=["System"])
def home():
    return {"message": "ParentCare Analytics API is running", "version": "2.0.0", "docs": "/docs"}


@app.get("/health", tags=["System"])
def health():
    return {"status": "healthy"}


@app.get("/model-info", tags=["System"], summary="ML model details and real accuracy")
def model_info():
    return get_model_metadata()


# ── Assessment ────────────────────────────────────────────

@app.post("/assess-child", tags=["Assessment"],
          response_model=AssessmentResponse,
          summary="Complete child wellness assessment",
          dependencies=[Depends(verify_api_key)])
@limiter.limit("30/minute")
def assess(request: Request, body: ChildAssessmentRequest):
    try:
        logger.info(f"Assessment | age={body.age} | screen={body.screen_time}hrs")

        rule = assess_child(
            age=body.age, screen_time=body.screen_time,
            poor_sleep=body.poor_sleep, eye_strain=body.eye_strain,
            anxiety=body.anxiety, obesity_risk=body.obesity_risk,
            educational_ratio=body.educational_ratio,
        )
        ml = predict_wellness(
            age=body.age, screen_time=body.screen_time,
            educational_ratio=body.educational_ratio,
            poor_sleep=body.poor_sleep, eye_strain=body.eye_strain,
            anxiety=body.anxiety, obesity_risk=body.obesity_risk,
        )
        recs = generate_recommendations(
    wellness_category=rule["wellness_category"],
    poor_sleep=body.poor_sleep,
    eye_strain=body.eye_strain,
    anxiety=body.anxiety,
    obesity_risk=body.obesity_risk,
    educational_ratio=body.educational_ratio,
    urban_or_rural=body.urban_or_rural
)
        activities = generate_activity_suggestions(
    age_group=rule["age_group"],
    wellness_category=rule["wellness_category"],
    urban_or_rural=body.urban_or_rural
)
        diet = generate_diet_tips(
    poor_sleep=body.poor_sleep,
    eye_strain=body.eye_strain,
    anxiety=body.anxiety,
    obesity_risk=body.obesity_risk,
    urban_or_rural=body.urban_or_rural
)

        return {**rule,
                "ml_prediction":    ml["ml_prediction"],
                "ml_confidence":    ml["ml_confidence"],
                "probabilities":    ml["probabilities"],
                "recommendations":  recs,
                "activity_suggestions": activities,
                "diet_tips":        diet}

    except ValueError as e:
        raise HTTPException(status_code=422, detail=str(e))
    except Exception as e:
        logger.error(f"Assessment error: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=str(e))


# ── Analytics ─────────────────────────────────────────────

@app.get("/dashboard-summary", tags=["Analytics"])
@limiter.limit("60/minute")
def dashboard_summary(request: Request):
    return get_dashboard_summary()


@app.get("/wellness-distribution", tags=["Analytics"])
@limiter.limit("60/minute")
def wellness_dist(request: Request):
    return get_wellness_distribution()


@app.get("/age-group-analysis", tags=["Analytics"])
@limiter.limit("60/minute")
def age_analysis(request: Request):
    return get_age_group_analysis()


@app.get("/health-concerns", tags=["Analytics"])
@limiter.limit("60/minute")
def health_concern_counts(request: Request):
    return get_health_concerns()


@app.get("/device-analysis", tags=["Analytics"])
@limiter.limit("60/minute")
def device_analysis(request: Request):
    return get_device_analysis()


@app.get("/urban-rural-comparison", tags=["Analytics"])
@limiter.limit("60/minute")
def urban_rural(request: Request):
    return get_urban_rural()
