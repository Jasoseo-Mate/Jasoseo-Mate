from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0004_deduplicate_jobposts"),
    ]

    operations = [
        migrations.AddConstraint(
            model_name="jobpost",
            constraint=models.UniqueConstraint(
                fields=("company_name", "title"),
                name="unique_job_company_title",
            ),
        ),
    ]
