from django.core.management.base import BaseCommand
from django.db import transaction

from jobs.models import JobPost, Skill

SKILL_NAMES = [
    "Python",
    "Django",
    "Java",
    "Spring",
    "JavaScript",
    "TypeScript",
    "React",
    "Vue.js",
    "HTML/CSS",
    "SQL",
    "MySQL",
    "PostgreSQL",
    "AWS",
    "Docker",
    "Git",
    "REST API",
    "데이터 분석",
    "머신러닝",
    "마케팅/광고/홍보",
    "콘텐츠 기획",
    "서비스 기획",
    "프로젝트 관리",
    "UI/UX",
    "Figma",
    "영업",
    "고객 관리",
    "재무/회계",
    "인사/채용",
    "커뮤니케이션",
    "문제 해결",
]


SAMPLE_JOBS = [
    (
        "메이트테크(샘플)",
        "주니어 백엔드 개발자",
        "스타트업",
        ["Python", "Django", "REST API", "PostgreSQL"],
        "채용 서비스 API와 데이터 모델을 개발합니다.",
    ),
    (
        "푸른클라우드(샘플)",
        "클라우드 플랫폼 엔지니어",
        "중견기업",
        ["AWS", "Docker", "Python", "Git"],
        "클라우드 인프라와 배포 자동화를 운영합니다.",
    ),
    (
        "한빛소프트랩(샘플)",
        "Java 서버 개발자",
        "중소기업",
        ["Java", "Spring", "MySQL", "REST API"],
        "기업용 웹 서비스의 서버 기능을 개발합니다.",
    ),
    (
        "모아커머스(샘플)",
        "프론트엔드 개발자",
        "중소기업",
        ["JavaScript", "TypeScript", "React", "HTML/CSS"],
        "커머스 고객 화면과 운영 도구를 개발합니다.",
    ),
    (
        "새봄데이터(샘플)",
        "데이터 분석가",
        "스타트업",
        ["Python", "SQL", "데이터 분석", "커뮤니케이션"],
        "서비스 지표를 분석하고 의사결정을 지원합니다.",
    ),
    (
        "넥스트인사이트(샘플)",
        "머신러닝 엔지니어",
        "중소기업",
        ["Python", "머신러닝", "데이터 분석", "Docker"],
        "추천 모델을 개발하고 서비스에 적용합니다.",
    ),
    (
        "다온플랫폼(샘플)",
        "웹 서비스 개발자",
        "중견기업",
        ["Vue.js", "JavaScript", "Java", "Spring"],
        "사내 업무 플랫폼의 웹 기능을 개발합니다.",
    ),
    (
        "우리핀테크(샘플)",
        "금융 백엔드 개발자",
        "대기업",
        ["Java", "Spring", "SQL", "문제 해결"],
        "안정적인 금융 거래 시스템을 개발합니다.",
    ),
    (
        "픽셀웨이브(샘플)",
        "UI/UX 디자이너",
        "스타트업",
        ["UI/UX", "Figma", "서비스 기획", "커뮤니케이션"],
        "사용자 조사와 제품 인터페이스 설계를 담당합니다.",
    ),
    (
        "브랜드메이트(샘플)",
        "디지털 마케터",
        "중소기업",
        ["마케팅/광고/홍보", "콘텐츠 기획", "데이터 분석", "커뮤니케이션"],
        "캠페인을 기획하고 성과 데이터를 분석합니다.",
    ),
    (
        "콘텐츠숲(샘플)",
        "콘텐츠 기획자",
        "스타트업",
        ["콘텐츠 기획", "마케팅/광고/홍보", "서비스 기획", "커뮤니케이션"],
        "취업 교육 콘텐츠를 기획하고 운영합니다.",
    ),
    (
        "모두의서비스(샘플)",
        "주니어 서비스 기획자",
        "중견기업",
        ["서비스 기획", "프로젝트 관리", "UI/UX", "데이터 분석"],
        "고객 요구사항을 제품 기능으로 구체화합니다.",
    ),
    (
        "성장파트너스(샘플)",
        "B2B 영업 담당자",
        "중소기업",
        ["영업", "고객 관리", "커뮤니케이션", "문제 해결"],
        "기업 고객을 발굴하고 장기 관계를 관리합니다.",
    ),
    (
        "고객의마음(샘플)",
        "고객 성공 매니저",
        "스타트업",
        ["고객 관리", "커뮤니케이션", "서비스 기획", "문제 해결"],
        "고객의 제품 도입과 활용을 지원합니다.",
    ),
    (
        "바른경영(샘플)",
        "재무회계 담당자",
        "중견기업",
        ["재무/회계", "SQL", "커뮤니케이션", "문제 해결"],
        "회계 결산과 경영 지표 관리를 담당합니다.",
    ),
    (
        "사람과성장(샘플)",
        "채용 운영 담당자",
        "중소기업",
        ["인사/채용", "커뮤니케이션", "프로젝트 관리", "고객 관리"],
        "채용 과정과 지원자 경험을 운영합니다.",
    ),
    (
        "오픈프로젝트(샘플)",
        "IT 프로젝트 매니저",
        "대기업",
        ["프로젝트 관리", "서비스 기획", "커뮤니케이션", "문제 해결"],
        "개발 프로젝트의 일정과 협업을 관리합니다.",
    ),
    (
        "데이터브릿지(샘플)",
        "데이터 엔지니어",
        "중견기업",
        ["Python", "SQL", "PostgreSQL", "AWS"],
        "분석용 데이터 파이프라인을 구축합니다.",
    ),
    (
        "프론트가든(샘플)",
        "Vue.js 프론트엔드 개발자",
        "스타트업",
        ["Vue.js", "TypeScript", "HTML/CSS", "Git"],
        "반응형 웹 애플리케이션을 개발합니다.",
    ),
    (
        "안심시스템(샘플)",
        "DevOps 엔지니어",
        "중소기업",
        ["AWS", "Docker", "Git", "Python"],
        "서비스 배포 환경과 모니터링 체계를 운영합니다.",
    ),
]


class Command(BaseCommand):
    help = "로컬 개발과 시연을 위한 스킬 및 샘플 채용 공고를 적재합니다."

    def add_arguments(self, parser):
        parser.add_argument(
            "--clear",
            action="store_true",
            help="샘플 공고만 삭제합니다. 스킬과 다른 출처의 공고는 유지합니다.",
        )

    @transaction.atomic
    def handle(self, *args, **options):
        if options["clear"]:
            sample_jobs = JobPost.objects.filter(source=JobPost.Source.SAMPLE)
            deleted_count = sample_jobs.count()
            sample_jobs.delete()
            self.stdout.write(self.style.SUCCESS(f"샘플 공고 {deleted_count}개를 삭제했습니다."))
            return

        skills = {}
        created_skill_count = 0
        for name in SKILL_NAMES:
            skill, created = Skill.objects.get_or_create(name=name)
            skills[name] = skill
            created_skill_count += int(created)

        created_job_count = 0
        updated_job_count = 0
        for company_name, title, company_size, skill_names, summary in SAMPLE_JOBS:
            description = (
                "[샘플 공고]\n"
                f"{summary}\n\n"
                "이 공고는 자소서 메이트의 기능 시연을 위해 만든 가상 데이터이며 "
                "실제 채용 공고가 아닙니다."
            )
            job, created = JobPost.objects.update_or_create(
                company_name=company_name,
                title=title,
                defaults={
                    "description": description,
                    "company_size": company_size,
                    "source": JobPost.Source.SAMPLE,
                },
            )
            job.required_skills.set(skills[name] for name in skill_names)
            created_job_count += int(created)
            updated_job_count += int(not created)

        self.stdout.write(
            self.style.SUCCESS(
                f"시드 완료: 신규 스킬 {created_skill_count}개, "
                f"신규 공고 {created_job_count}개, 갱신 공고 {updated_job_count}개."
            )
        )
