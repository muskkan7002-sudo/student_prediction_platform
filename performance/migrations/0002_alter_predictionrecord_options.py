from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ("performance", "0001_initial"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="predictionrecord",
            options={
                "ordering": ["-created_at"],
                "verbose_name": "Prediction record",
                "verbose_name_plural": "Prediction records",
            },
        ),
    ]
