from django.db import migrations


def deduplicate_job_posts(apps, schema_editor):
    JobPost = apps.get_model("jobs", "JobPost")
    CoverLetter = apps.get_model("resumes", "CoverLetter")
    database = schema_editor.connection.alias

    seen = {}
    for job in JobPost.objects.using(database).order_by("pk"):
        key = (job.company_name, job.title)
        canonical = seen.get(key)
        if canonical is None:
            seen[key] = job
            continue

        canonical.required_skills.add(*job.required_skills.all())
        CoverLetter.objects.using(database).filter(job_post_id=job.pk).update(
            job_post_id=canonical.pk
        )
        job.delete()


class Migration(migrations.Migration):
    dependencies = [
        ("jobs", "0003_jobpost_company_size"),
        ("resumes", "0001_initial"),
    ]

    operations = [
        migrations.RunPython(deduplicate_job_posts, migrations.RunPython.noop),
    ]
