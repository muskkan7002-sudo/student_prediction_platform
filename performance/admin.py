from django.contrib import admin

from .models import PredictionRecord

admin.site.site_header = "EduInsight Administration"
admin.site.site_title = "EduInsight Admin"
admin.site.index_title = "Workspace overview"


@admin.register(PredictionRecord)
class PredictionRecordAdmin(admin.ModelAdmin):
    list_display = (
        "student_name",
        "attendance",
        "study_hours",
        "previous_marks",
        "assignment_score",
        "sleep_hours",
        "prediction",
        "readiness_score",
        "attention_status",
        "created_at",
    )
    search_fields = ("student_name", "prediction")
    list_filter = ("prediction", "created_at")
    date_hierarchy = "created_at"
    readonly_fields = ("readiness_score", "attention_status", "created_at")
    list_per_page = 20
