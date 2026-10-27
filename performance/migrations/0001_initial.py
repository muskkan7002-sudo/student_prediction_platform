from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="PredictionRecord",
            fields=[
                ("id", models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name="ID")),
                ("student_name", models.CharField(max_length=100)),
                ("attendance", models.FloatField()),
                ("study_hours", models.FloatField()),
                ("previous_marks", models.FloatField()),
                ("assignment_score", models.FloatField()),
                ("sleep_hours", models.FloatField()),
                ("prediction", models.CharField(max_length=30)),
                ("suggestion", models.TextField()),
                ("created_at", models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
