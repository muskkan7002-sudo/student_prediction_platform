from pathlib import Path
import json
import logging

BASE_DIR = Path(__file__).resolve().parent.parent
MODEL_PATH = BASE_DIR / "ml_model" / "student_performance_model.pkl"
METRICS_PATH = BASE_DIR / "ml_model" / "model_metrics.json"
VALID_PREDICTIONS = {"Excellent", "Good", "Average", "Needs Improvement"}

logger = logging.getLogger(__name__)


def load_model_metrics():
    if not METRICS_PATH.exists():
        return None

    try:
        return json.loads(METRICS_PATH.read_text(encoding="utf-8"))
    except (json.JSONDecodeError, OSError):
        return None


def get_suggestion(prediction):
    suggestions = {
        "Excellent": "Excellent performance. Keep maintaining your study routine and attendance.",
        "Good": "Good performance. Try to increase consistency and keep attendance above 85%.",
        "Average": "Average performance. Improve daily study hours and submit assignments on time.",
        "Needs Improvement": "Needs improvement. Focus on attendance, revision, and regular practice.",
    }
    return suggestions.get(prediction, "Keep improving your learning habits.")


def rule_based_prediction(attendance, study_hours, previous_marks, assignment_score, sleep_hours):
    score = (
        attendance * 0.30
        + previous_marks * 0.35
        + assignment_score * 0.20
        + min(study_hours, 8) * 10 * 0.10
        + min(sleep_hours, 8) * 10 * 0.05
    )

    if score >= 85:
        return "Excellent"
    if score >= 70:
        return "Good"
    if score >= 55:
        return "Average"
    return "Needs Improvement"


def predict_performance(attendance, study_hours, previous_marks, assignment_score, sleep_hours):
    features = [[attendance, study_hours, previous_marks, assignment_score, sleep_hours]]

    if MODEL_PATH.exists():
        try:
            import joblib

            model = joblib.load(MODEL_PATH)
            prediction = model.predict(features)[0]
            if prediction in VALID_PREDICTIONS:
                return prediction
            logger.warning("Model returned an unknown prediction: %s", prediction)
        except (ImportError, OSError, ValueError) as error:
            logger.warning("Could not use ML model. Falling back to rules: %s", error)

    return rule_based_prediction(
        attendance,
        study_hours,
        previous_marks,
        assignment_score,
        sleep_hours,
    )
