from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0005_add_jobpost_unique_constraint"),
    ]

    operations = [
        migrations.AddField(
            model_name="jobpost",
            name="source",
            field=models.CharField(
                choices=[
                    ("manual", "직접 등록"),
                    ("sample", "샘플"),
                    ("work24", "고용24"),
                ],
                db_index=True,
                default="manual",
                max_length=10,
                verbose_name="데이터 출처",
            ),
        ),
    ]
