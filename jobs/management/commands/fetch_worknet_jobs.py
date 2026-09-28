import xml.etree.ElementTree as ET

import requests
from django.conf import settings
from django.core.management.base import BaseCommand, CommandError

from jobs.models import JobPost, Skill


WORK24_JOB_API_URL = (
    "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210L01.do"
)
WORK24_JOB_DETAIL_API_URL = (
    "https://www.work24.go.kr/cm/openApi/call/wk/callOpenApiSvcInfo210D01.do"
)


def first_text(node, *tags):
    for tag in tags:
        value = node.findtext(tag)
        if value and value.strip():
            return value.strip()
    return ""


def normalize_company_size(value):
    normalized = (value or "").replace(" ", "").lower()
    if "대기업" in normalized:
        return "대기업"
    if "중견" in normalized:
        return "중견기업"
    if "벤처" in normalized or "스타트업" in normalized:
        return "스타트업"
    if "중소" in normalized or "강소" in normalized:
        return "중소기업"
    return "무관"


class Command(BaseCommand):
    help = "고용24 OpenAPI 채용 공고를 데이터베이스에 동기화합니다."

    def handle(self, *args, **options):
        api_key = settings.WORKNET_API_KEY
        if not api_key:
            raise CommandError(
                "오류: .env 파일에 WORKNET_API_KEY가 등록되어 있지 않습니다."
            )

        self.stdout.write("고용24 OpenAPI에서 채용 정보를 가져오는 중...")
        params = {
            "authKey": api_key,
            "callTp": "L",
            "returnType": "XML",
            "startPage": "1",
            "display": "30",
        }

        try:
            response = requests.get(WORK24_JOB_API_URL, params=params, timeout=15)
            response.raise_for_status()
            root = ET.fromstring(response.text)
            self._raise_for_api_error(root)

            wanted_nodes = root.findall(".//wanted")
            if not wanted_nodes:
                self.stdout.write(
                    self.style.WARNING(
                        "가져온 채용 정보가 없습니다. API 키와 요청 조건을 확인해 주세요."
                    )
                )
                return

            skills = list(Skill.objects.all())
            created_count = 0
            updated_count = 0

            for wanted in wanted_nodes:
                company_name = first_text(wanted, "company", "corpNm")
                title = first_text(wanted, "title", "wantedTitle")
                if not company_name or not title:
                    continue

                wanted_auth_no = first_text(wanted, "wantedAuthNo")
                existing_job = JobPost.objects.filter(
                    company_name=company_name, title=title
                ).first()
                company_size = normalize_company_size(first_text(wanted, "busiSize"))
                if company_size == "무관" and existing_job is not None:
                    company_size = existing_job.company_size
                elif company_size == "무관" and wanted_auth_no:
                    company_size = self._fetch_company_size(api_key, wanted_auth_no)

                salary_type = first_text(wanted, "salTpNm")
                salary = first_text(wanted, "sal")
                career = first_text(wanted, "career")
                close_date = first_text(wanted, "closeDt")
                info_url = first_text(wanted, "wantedInfoUrl")
                industry = first_text(wanted, "indTpNm")

                description = f"""[고용24 채용 공고]
- 업종: {industry or '미제공'}
- 급여 요건: {(salary_type + ' ' + salary).strip() or '미제공'}
- 경력 요건: {career or '미제공'}
- 마감 기한: {close_date or '미제공'}
- 상세 공고: {info_url or '미제공'}

본 공고는 고용24 OpenAPI 동기화를 통해 생성된 채용 정보입니다."""

                job, created = JobPost.objects.get_or_create(
                    company_name=company_name,
                    title=title,
                    defaults={
                        "description": description,
                        "company_size": company_size,
                        "source": JobPost.Source.WORK24,
                    },
                )
                if created:
                    created_count += 1
                else:
                    job.description = description
                    job.company_size = company_size
                    job.source = JobPost.Source.WORK24
                    job.save(update_fields=["description", "company_size", "source"])
                    updated_count += 1

                job.required_skills.clear()
                target_text = f"{title} {career} {industry}".lower()
                for skill in skills:
                    keywords = (keyword.strip().lower() for keyword in skill.name.split("/"))
                    if any(keyword and keyword in target_text for keyword in keywords):
                        job.required_skills.add(skill)

            self.stdout.write(
                self.style.SUCCESS(
                    f"동기화 완료: 신규 {created_count}개, 업데이트 {updated_count}개."
                )
            )
        except CommandError:
            raise
        except requests.exceptions.RequestException as error:
            raise CommandError(f"고용24 API 통신에 실패했습니다: {error}") from error
        except ET.ParseError as error:
            raise CommandError(f"고용24 XML 응답을 분석하지 못했습니다: {error}") from error

    def _fetch_company_size(self, api_key, wanted_auth_no):
        params = {
            "authKey": api_key,
            "callTp": "D",
            "returnType": "XML",
            "wantedAuthNo": wanted_auth_no,
            "infoSvc": "VALIDATION",
        }
        try:
            response = requests.get(
                WORK24_JOB_DETAIL_API_URL, params=params, timeout=10
            )
            response.raise_for_status()
            root = ET.fromstring(response.text)
            self._raise_for_api_error(root)
            return normalize_company_size(first_text(root, ".//busiSize"))
        except (requests.exceptions.RequestException, ET.ParseError, CommandError) as error:
            self.stderr.write(
                self.style.WARNING(
                    f"{wanted_auth_no} 기업 규모 조회 실패: {error}. '무관'으로 저장합니다."
                )
            )
            return "무관"

    @staticmethod
    def _raise_for_api_error(root):
        message_node = root.find(".//message")
        if message_node is None:
            return
        message = (message_node.text or "알 수 없는 API 오류").strip()
        if "유효" in message:
            raise CommandError(
                "고용24 API 키가 만료되었거나 유효하지 않습니다. 데이터는 변경하지 않았습니다."
            )
        raise CommandError(f"고용24 API 오류: {message}")
