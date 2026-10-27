from django.db import models


class PredictionRecord(models.Model):
    student_name = models.CharField(max_length=100)
    attendance = models.FloatField()
    study_hours = models.FloatField()
    previous_marks = models.FloatField()
    assignment_score = models.FloatField()
    sleep_hours = models.FloatField()
    prediction = models.CharField(max_length=30)
    suggestion = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Prediction record"
        verbose_name_plural = "Prediction records"

    def __str__(self):
        return f"{self.student_name} - {self.prediction}"

    @property
    def readiness_score(self):
        return round(
            self.attendance * 0.30
            + self.previous_marks * 0.35
            + self.assignment_score * 0.20
            + min(self.study_hours, 8) * 10 * 0.10
            + min(self.sleep_hours, 8) * 10 * 0.05,
            1,
        )

    @property
    def attention_status(self):
        if self.prediction in ["Average", "Needs Improvement"]:
            return "Needs attention"
        return "On track"
