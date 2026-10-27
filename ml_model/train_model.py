from pathlib import Path
import json

import joblib
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import (
    accuracy_score,
    classification_report,
    confusion_matrix,
    f1_score,
    precision_score,
    recall_score,
)
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.neighbors import KNeighborsClassifier
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.tree import DecisionTreeClassifier

BASE_DIR = Path(__file__).resolve().parent
DATA_PATH = BASE_DIR / "student_data.csv"
MODEL_PATH = BASE_DIR / "student_performance_model.pkl"
METRICS_PATH = BASE_DIR / "model_metrics.json"

FEATURE_COLUMNS = [
    "attendance",
    "study_hours",
    "previous_marks",
    "assignment_score",
    "sleep_hours",
]
TARGET_COLUMN = "performance"
CLASS_LABELS = ["Excellent", "Good", "Average", "Needs Improvement"]


def model_candidates():
    return {
        "Decision Tree": DecisionTreeClassifier(random_state=42),
        "Random Forest": RandomForestClassifier(n_estimators=120, random_state=42),
        "Logistic Regression": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", LogisticRegression(max_iter=1000, random_state=42)),
            ]
        ),
        "K-Nearest Neighbors": Pipeline(
            [
                ("scaler", StandardScaler()),
                ("model", KNeighborsClassifier(n_neighbors=3)),
            ]
        ),
        "Naive Bayes": GaussianNB(),
    }


def extract_feature_importance(model):
    estimator = model.named_steps["model"] if hasattr(model, "named_steps") else model

    if hasattr(estimator, "feature_importances_"):
        scores = estimator.feature_importances_
    elif hasattr(estimator, "coef_"):
        scores = abs(estimator.coef_).mean(axis=0)
    else:
        return []

    return [
        {"feature": feature, "importance": round(float(score), 4)}
        for feature, score in sorted(
            zip(FEATURE_COLUMNS, scores),
            key=lambda item: item[1],
            reverse=True,
        )
    ]


def train_model():
    data = pd.read_csv(DATA_PATH)

    features = data[FEATURE_COLUMNS]
    target = data[TARGET_COLUMN]

    x_train, x_test, y_train, y_test = train_test_split(
        features,
        target,
        test_size=0.30,
        random_state=42,
        stratify=target,
    )

    results = []
    trained_models = {}

    for name, model in model_candidates().items():
        model.fit(x_train, y_train)
        predictions = model.predict(x_test)

        results.append(
            {
                "name": name,
                "accuracy": round(accuracy_score(y_test, predictions), 4),
                "precision": round(
                    precision_score(y_test, predictions, average="weighted", zero_division=0),
                    4,
                ),
                "recall": round(
                    recall_score(y_test, predictions, average="weighted", zero_division=0),
                    4,
                ),
                "f1_score": round(
                    f1_score(y_test, predictions, average="weighted", zero_division=0),
                    4,
                ),
            }
        )
        trained_models[name] = (model, predictions)

    best_result = max(results, key=lambda item: (item["accuracy"], item["f1_score"]))
    best_model, best_predictions = trained_models[best_result["name"]]

    best_model.fit(features, target)

    metrics = {
        "best_model": best_result["name"],
        "dataset_rows": int(len(data)),
        "training_rows": int(len(x_train)),
        "testing_rows": int(len(x_test)),
        "feature_columns": FEATURE_COLUMNS,
        "target_column": TARGET_COLUMN,
        "classes": CLASS_LABELS,
        "model_results": sorted(results, key=lambda item: item["accuracy"], reverse=True),
        "classification_report": classification_report(
            y_test,
            best_predictions,
            labels=CLASS_LABELS,
            output_dict=True,
            zero_division=0,
        ),
        "confusion_matrix": confusion_matrix(
            y_test,
            best_predictions,
            labels=CLASS_LABELS,
        ).tolist(),
        "feature_importance": extract_feature_importance(best_model),
    }

    joblib.dump(best_model, MODEL_PATH)
    METRICS_PATH.write_text(json.dumps(metrics, indent=2), encoding="utf-8")
    print(f"Best model: {best_result['name']}")
    print(f"Accuracy: {best_result['accuracy'] * 100:.2f}%")
    print(f"Model saved at: {MODEL_PATH}")
    print(f"Metrics saved at: {METRICS_PATH}")


if __name__ == "__main__":
    train_model()
