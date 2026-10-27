from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Count
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render

from .forms import StudentPredictionForm
from .ml_utils import get_suggestion, load_model_metrics, predict_performance
from .models import PredictionRecord


def build_insights(record):
    insights = []

    if record.attendance < 75:
        insights.append(("Attendance Risk", "Attendance is below the usual 75% benchmark."))
    else:
        insights.append(("Attendance Stable", "Attendance supports consistent classroom learning."))

    if record.study_hours < 3:
        insights.append(("Study Routine", "Daily study time needs a stronger routine."))
    elif record.study_hours >= 5:
        insights.append(("Study Routine", "Study hours show strong preparation discipline."))

    if record.assignment_score < 60:
        insights.append(("Assignment Focus", "Assignment score may reduce the overall outcome."))
    else:
        insights.append(("Assignment Focus", "Assignment performance is helping the prediction."))

    if record.sleep_hours < 6:
        insights.append(("Wellbeing Alert", "Sleep hours are low and may affect concentration."))
    elif record.sleep_hours > 9:
        insights.append(("Wellbeing Alert", "Sleep hours are high; balance routine with active study."))
    else:
        insights.append(("Wellbeing Stable", "Sleep pattern looks healthy for learning."))

    return insights


def result_theme(prediction):
    themes = {
        "Excellent": "success",
        "Good": "good",
        "Average": "warning",
        "Needs Improvement": "danger",
    }
    return themes.get(prediction, "warning")


def home(request):
    recent_predictions = PredictionRecord.objects.order_by("-created_at")[:5]
    total_predictions = PredictionRecord.objects.count()
    latest_prediction = recent_predictions[0] if recent_predictions else None
    strong_results = PredictionRecord.objects.filter(prediction__in=["Excellent", "Good"]).count()
    improvement_cases = PredictionRecord.objects.filter(prediction="Needs Improvement").count()
    success_rate = round((strong_results / total_predictions) * 100) if total_predictions else 0

    context = {
        "recent_predictions": recent_predictions,
        "total_predictions": total_predictions,
        "latest_prediction": latest_prediction,
        "success_rate": success_rate,
        "improvement_cases": improvement_cases,
    }
    return render(request, "performance/home.html", context)


@login_required
def dashboard(request):
    metrics = load_model_metrics()
    confusion_rows = []
    model_chart = []
    feature_chart = []
    if metrics:
        confusion_rows = zip(metrics.get("classes", []), metrics.get("confusion_matrix", []))
        model_chart = [
            {
                "name": model["name"],
                "accuracy": model["accuracy"],
                "percent": round(model["accuracy"] * 100, 1),
            }
            for model in metrics.get("model_results", [])
        ]
        max_importance = max(
            [item["importance"] for item in metrics.get("feature_importance", [])] or [1]
        )
        feature_chart = [
            {
                "feature": item["feature"].replace("_", " ").title(),
                "importance": item["importance"],
                "percent": round((item["importance"] / max_importance) * 100, 1),
            }
            for item in metrics.get("feature_importance", [])
        ]

    total_predictions = PredictionRecord.objects.count()
    raw_counts = {
        item["prediction"]: item["total"]
        for item in PredictionRecord.objects.values("prediction").annotate(total=Count("id"))
    }
    prediction_counts = [
        {
            "prediction": label,
            "total": raw_counts.get(label, 0),
            "percent": round((raw_counts.get(label, 0) / total_predictions) * 100, 1)
            if total_predictions
            else 0,
        }
        for label in ["Excellent", "Good", "Average", "Needs Improvement"]
    ]
    averages = PredictionRecord.objects.aggregate(
        avg_attendance=Avg("attendance"),
        avg_study_hours=Avg("study_hours"),
        avg_previous_marks=Avg("previous_marks"),
        avg_assignment_score=Avg("assignment_score"),
        avg_sleep_hours=Avg("sleep_hours"),
    )
    attention_count = PredictionRecord.objects.filter(
        prediction__in=["Average", "Needs Improvement"]
    ).count()
    attention_rate = round((attention_count / total_predictions) * 100) if total_predictions else 0

    context = {
        "total_predictions": total_predictions,
        "prediction_counts": prediction_counts,
        "averages": averages,
        "attention_rate": attention_rate,
        "metrics": metrics,
        "confusion_rows": confusion_rows,
        "model_chart": model_chart,
        "feature_chart": feature_chart,
    }
    return render(request, "performance/dashboard.html", context)


def predict(request):
    if request.method == "POST":
        form = StudentPredictionForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            prediction = predict_performance(
                data["attendance"],
                data["study_hours"],
                data["previous_marks"],
                data["assignment_score"],
                data["sleep_hours"],
            )
            suggestion = get_suggestion(prediction)

            record = PredictionRecord.objects.create(
                student_name=data["student_name"],
                attendance=data["attendance"],
                study_hours=data["study_hours"],
                previous_marks=data["previous_marks"],
                assignment_score=data["assignment_score"],
                sleep_hours=data["sleep_hours"],
                prediction=prediction,
                suggestion=suggestion,
            )

            context = {
                "record": record,
                "readiness_score": record.readiness_score,
                "insights": build_insights(record),
                "theme": result_theme(record.prediction),
            }
            return render(request, "performance/result.html", context)
    else:
        form = StudentPredictionForm()

    return render(request, "performance/predict.html", {"form": form})


def about(request):
    return render(request, "performance/about.html")


def pdf_escape(value):
    return str(value).replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def make_prediction_pdf(record):
    lines = [
        "Student Performance Prediction Report",
        f"Student Name: {record.student_name}",
        f"Prediction: {record.prediction}",
        f"Readiness Score: {record.readiness_score}%",
        f"Attendance: {record.attendance}%",
        f"Study Hours per Day: {record.study_hours}",
        f"Previous Marks: {record.previous_marks}%",
        f"Assignment Score: {record.assignment_score}%",
        f"Sleep Hours per Day: {record.sleep_hours}",
        f"Suggestion: {record.suggestion}",
        f"Generated On: {record.created_at.strftime('%d %b %Y, %I:%M %p')}",
    ]
    text_commands = ["BT", "/F1 18 Tf", "72 760 Td"]
    for index, line in enumerate(lines):
        if index == 1:
            text_commands.extend(["/F1 12 Tf", "0 -32 Td"])
        elif index > 1:
            text_commands.append("0 -24 Td")
        text_commands.append(f"({pdf_escape(line)}) Tj")
    text_commands.append("ET")
    stream = "\n".join(text_commands).encode("latin-1", errors="replace")

    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] "
        b"/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"\nendstream",
    ]
    pdf = [b"%PDF-1.4\n"]
    offsets = []
    for number, obj in enumerate(objects, start=1):
        offsets.append(sum(len(part) for part in pdf))
        pdf.append(f"{number} 0 obj\n".encode("ascii") + obj + b"\nendobj\n")
    xref_offset = sum(len(part) for part in pdf)
    pdf.append(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    pdf.append(b"0000000000 65535 f \n")
    for offset in offsets:
        pdf.append(f"{offset:010d} 00000 n \n".encode("ascii"))
    pdf.append(
        f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
        f"startxref\n{xref_offset}\n%%EOF\n".encode("ascii")
    )
    return b"".join(pdf)


def prediction_report_pdf(request, pk):
    record = get_object_or_404(PredictionRecord, pk=pk)
    response = HttpResponse(make_prediction_pdf(record), content_type="application/pdf")
    response["Content-Disposition"] = (
        f'attachment; filename="student-performance-report-{record.pk}.pdf"'
    )
    return response
