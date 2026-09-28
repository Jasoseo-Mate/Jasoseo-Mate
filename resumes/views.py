from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render

from jobs.models import JobPost  # CoverLetter와 연결하기 위해 필요

from .forms import CoverLetterForm, ExperienceForm, ResumeForm
from .models import CoverLetter, Experience, Resume


@login_required
def experience_list(request):
    experiences = request.user.experiences.all()
    context = {"experiences": experiences}
    return render(request, "resumes/experience_list.html", context)


@login_required
def experience_create(request):
    form = ExperienceForm(request.POST or None)
    if form.is_valid():
        experience = form.save(commit=False)
        experience.user = request.user
        experience.save()
        return redirect("resumes:experience_list")
    return render(request, "resumes/experience_form.html", {"form": form})


@login_required
def experience_update(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    form = ExperienceForm(request.POST or None, instance=experience)
    if form.is_valid():
        form.save()
        return redirect("resumes:experience_list")
    context = {"experience": experience, "form": form}
    return render(request, "resumes/experience_form.html", context)


@login_required
def experience_delete(request, pk):
    experience = get_object_or_404(Experience, pk=pk, user=request.user)
    if request.method == "POST":
        experience.delete()
        return redirect("resumes:experience_list")
    context = {"experience": experience}
    return render(request, "resumes/experience_confirm_delete.html", context)


# Resume 관련 뷰
@login_required
def resume_list(request):
    resumes = request.user.resumes.all()
    context = {"resumes": resumes}
    return render(request, "resumes/resume_list.html", context)


@login_required
def resume_create(request):
    form = ResumeForm(request.POST or None)
    if form.is_valid():
        resume = form.save(commit=False)
        resume.user = request.user
        resume.save()
        return redirect("resumes:resume_list")
    return render(request, "resumes/resume_form.html", {"form": form})


@login_required
def resume_update(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    form = ResumeForm(request.POST or None, instance=resume)
    if form.is_valid():
        form.save()
        return redirect("resumes:resume_list")
    context = {"resume": resume, "form": form}
    return render(request, "resumes/resume_form.html", context)


@login_required
def resume_delete(request, pk):
    resume = get_object_or_404(Resume, pk=pk, user=request.user)
    if request.method == "POST":
        resume.delete()
        return redirect("resumes:resume_list")
    context = {"resume": resume}
    return render(request, "resumes/resume_confirm_delete.html", context)


# CoverLetter 관련 뷰
@login_required
def coverletter_list(request):
    coverletters = request.user.cover_letters.all()
    context = {"coverletters": coverletters}
    return render(request, "resumes/coverletter_list.html", context)


@login_required
def coverletter_create(request, job_post_pk):
    job_post = get_object_or_404(JobPost, pk=job_post_pk)
    default_title = f"{job_post.company_name} 지원 자기소개서"
    default_content = """1. 본인의 성장과정 및 지원동기를 기술해 주시기 바랍니다.


2. 직무와 관련하여 본인이 수행했던 프로젝트 또는 경험을 구체적으로 기술해 주시기 바랍니다.


3. 성격의 장단점 및 이를 극복/활용하기 위해 노력한 점을 기술해 주시기 바랍니다.


4. 입사 후 포부 및 향후 성장 계획을 기술해 주시기 바랍니다.
"""
    form = CoverLetterForm(
        request.POST or None,
        initial={"title": default_title, "content": default_content},
    )
    if form.is_valid():
        coverletter = form.save(commit=False)
        coverletter.user = request.user
        coverletter.job_post = job_post
        coverletter.target_company = job_post.company_name
        coverletter.target_role = job_post.title
        coverletter.save()
        return redirect("resumes:coverletter_list")  # 또는 해당 job_post 상세 페이지
    context = {
        "job_post": job_post,
        "form": form,
        "default_title": default_title,
        "default_content": default_content,
    }
    return render(request, "resumes/coverletter_form.html", context)


@login_required
def coverletter_update(request, pk):
    coverletter = get_object_or_404(CoverLetter, pk=pk, user=request.user)
    form = CoverLetterForm(request.POST or None, instance=coverletter)
    if form.is_valid():
        form.save()
        return redirect("resumes:coverletter_list")
    context = {"coverletter": coverletter, "form": form}
    return render(request, "resumes/coverletter_form.html", context)


@login_required
def coverletter_delete(request, pk):
    coverletter = get_object_or_404(CoverLetter, pk=pk, user=request.user)
    if request.method == "POST":
        coverletter.delete()
        return redirect("resumes:coverletter_list")
    context = {"coverletter": coverletter}
    return render(request, "resumes/coverletter_confirm_delete.html", context)
