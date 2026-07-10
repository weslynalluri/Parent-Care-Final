import pickle, json, logging
from pathlib import Path
import pandas as pd

logger = logging.getLogger(__name__)

_BASE     = Path(__file__).resolve().parent.parent / "models"
_MODEL    = _BASE / "wellness_model.pkl"
_METADATA = _BASE / "model_metadata.json"

_FEATURES = ["Age", "Avg_Daily_Screen_Time_hr", "Educational_to_Recreational_Ratio",
             "Poor_Sleep", "Eye_Strain", "Anxiety", "Obesity_Risk"]

try:
    with open(_MODEL, "rb") as f:    _clf  = pickle.load(f)
    with open(_METADATA, "r") as f:  _meta = json.load(f)
    logger.info(f"Model loaded. Accuracy: {_meta['accuracy']}%")
except Exception as e:
    logger.error(f"Model load failed: {e}")
    _clf, _meta = None, {}


def get_model_metadata() -> dict:
    return _meta


def predict_wellness(age, screen_time, educational_ratio,
                     poor_sleep, eye_strain, anxiety, obesity_risk) -> dict:
    if _clf is None:
        return {"ml_prediction": "Unavailable", "ml_confidence": 0.0,
                "probabilities": {}, "feature_importances": {}}

    row = pd.DataFrame(
        [[age, screen_time, educational_ratio,
          int(poor_sleep), int(eye_strain), int(anxiety), int(obesity_risk)]],
        columns=_FEATURES
    )
    prediction    = _clf.predict(row)[0]
    probs         = _clf.predict_proba(row)[0]
    confidence    = round(float(max(probs)) * 100, 1)
    prob_dict     = {cls: round(float(p)*100,1) for cls,p in zip(_clf.classes_, probs)}
    importance    = {f: round(float(i)*100,1) for f,i in zip(_FEATURES, _clf.feature_importances_)}

    return {
        "ml_prediction":     prediction,
        "ml_confidence":     confidence,
        "probabilities":     prob_dict,
        "feature_importances": importance,
    }
