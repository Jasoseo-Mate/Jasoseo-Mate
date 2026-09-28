import django.db.models.deletion
from django.db import migrations, models


def populate_targets(apps, schema_editor):
    CoverLetter = apps.get_model("resumes", "CoverLetter")
    for coverletter in CoverLetter.objects.select_related("job_post"):
        if coverletter.job_post_id:
            coverletter.target_company = coverletter.job_post.company_name
            coverletter.target_role = coverletter.job_post.title
            coverletter.save(update_fields=["target_company", "target_role"])


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0004_deduplicate_jobposts"),
        ("resumes", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="coverletter",
            name="job_post",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="cover_letters",
                to="jobs.jobpost",
            ),
        ),
        migrations.AddField(
            model_name="coverletter",
            name="target_company",
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AddField(
            model_name="coverletter",
            name="target_role",
            field=models.CharField(blank=True, max_length=200),
        ),
        migrations.RunPython(populate_targets, migrations.RunPython.noop),
    ]
