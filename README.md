# 자소서 메이트 (Jasoseo Mate)

> 흩어진 취업 준비 정보를 하나로 모으고, 내 경험을 실제 지원서로 연결하는 AI 취업 준비 서비스

취업을 준비하다 보면 학력, 자격증, 프로젝트, 대외활동, 경력은 여러 문서에 흩어지고, 채용 공고마다 어떤 경험을 강조해야 할지 다시 고민하게 됩니다. 자소서 메이트는 사용자의 스펙과 경험을 한곳에 정리하고, 그 정보를 바탕으로 어울리는 기업과 직무를 추천하며, 자기소개서 초안 작성까지 이어주는 서비스입니다.

## 프로젝트를 만든 이유

취업 준비 과정에는 반복되는 어려움이 있습니다.

- 내 경험과 강점을 객관적으로 정리하기 어렵습니다.
- 보유 역량과 잘 맞는 채용 공고를 판단하기 어렵습니다.
- 기업마다 어떤 경험을 자기소개서에 활용해야 할지 막막합니다.
- 작성한 이력서와 자기소개서가 여러 파일과 서비스에 흩어집니다.

자소서 메이트는 이 과정을 `스펙 정리 → 역량 분석 → 기업·공고 추천 → 자기소개서 작성 → 문서 관리`라는 하나의 흐름으로 연결합니다.

## 핵심 기능

### 1. 나만의 스펙 보드

학력, 자격증, 대내외 활동, 프로젝트, 경력과 경험을 항목별로 기록할 수 있습니다. 보유 역량과 희망 기업 규모도 함께 관리하여 이후 추천과 AI 분석에 활용합니다.

입력된 경험을 바탕으로 AI가 사용자가 보유했을 가능성이 높은 역량을 추천해 주기 때문에, 자신의 강점을 직접 정의하기 어려운 사용자도 프로필을 구체화할 수 있습니다.

### 2. 맞춤 채용 공고 추천

사용자의 보유 역량과 채용 공고의 요구 역량을 비교해 매칭률을 계산합니다. 사용자가 설정한 희망 기업 규모도 추천 점수에 반영합니다.

개인 개발 환경에서는 출처가 명확한 샘플 공고를 사용합니다. 고용24 OpenAPI 사용 권한이 있는 기관·기업 환경에서는 별도 동기화 커맨드로 실제 공고를 적재할 수 있으며, 추천 결과에서 데이터 출처와 요구 역량, 기업 규모를 함께 확인할 수 있습니다.

### 3. AI 기업·직무 매칭

사용자가 기록한 전공, 자격증, 활동, 프로젝트와 경력을 종합해 강점을 분석합니다. 분석 결과를 바탕으로 어울리는 기업과 직무, 추천 이유, 예상 매칭률을 제안합니다.

단순히 기업 이름만 보여주는 것이 아니라, 자기소개서에 활용하기 좋은 질문까지 함께 제안하여 다음 행동으로 자연스럽게 이어지도록 구성했습니다.

### 4. AI 자기소개서 작성

추천받은 기업, 직무, 자기소개서 문항과 사용자의 실제 경험을 조합해 초안을 생성합니다. 생성된 내용은 사용자가 직접 수정할 수 있으며, 완성한 자기소개서는 내 문서에 저장됩니다.

AI가 추천한 기업을 실제 채용 공고처럼 저장하지 않고 자기소개서의 지원 대상 정보로만 관리해, 실제 공고 데이터와 AI 추천 데이터가 섞이지 않도록 설계했습니다.

### 5. 기업 분석

관심 기업을 입력하면 기업의 비전, 인재상, 최근 이슈와 면접 팁을 AI가 정리합니다. 기업 관련 최신 기사도 함께 제공해 지원 전에 필요한 정보를 한 화면에서 살펴볼 수 있습니다.

### 6. 이력서와 자기소개서 관리

작성한 이력서, 자기소개서와 경력 정보를 계정별로 보관합니다. 사용자는 이전에 작성한 문서를 다시 확인하고 수정하거나 삭제할 수 있습니다.

### 7. 취업 준비 커뮤니티

취업 준비 과정에서 얻은 정보와 고민을 게시글과 댓글로 나눌 수 있습니다. 게시글 조회수와 댓글 수를 확인할 수 있으며, 작성자만 자신의 글과 댓글을 수정하거나 삭제할 수 있습니다.

## 사용자 흐름

```text
회원가입
   ↓
학력·자격증·활동·프로젝트·경력 입력
   ↓
보유 역량과 희망 기업 규모 설정
   ↓
맞춤 채용 공고 또는 AI 추천 기업 확인
   ↓
지원 기업과 자기소개서 문항 선택
   ↓
AI 초안 생성 및 직접 수정
   ↓
내 자기소개서에 저장
```

## 자소서 메이트의 특징

- 사용자가 직접 입력한 경험을 모든 추천과 생성의 출발점으로 사용합니다.
- 스펙 관리와 자기소개서 작성을 분리하지 않고 하나의 사용자 여정으로 연결합니다.
- 사용자의 역량이 많다는 이유로 매칭률이 낮아지지 않도록 공고 요구 역량 충족도를 중심으로 계산합니다.
- 희망 기업 규모를 매칭에 반영해 기술 역량 외의 선호 조건도 고려합니다.
- AI 추천 기업과 실제 채용 공고를 구분해 데이터의 신뢰성을 유지합니다.
- 사용자별 데이터 접근 범위를 분리하여 다른 사용자의 스펙이나 문서를 수정할 수 없도록 보호합니다.

## 서비스 구성

| 영역 | 제공 기능 |
| --- | --- |
| 내 스펙 | 프로필, 학력, 자격증, 활동, 프로젝트, 보유 역량 관리 |
| 경력·문서 | 경력, 이력서, 자기소개서 관리 |
| 채용 | 샘플 공고 제공, 선택적 고용24 공고 수집, 역량 기반 공고 매칭 |
| AI 지원 | 역량 추천, 기업 분석, 기업·직무 추천, 자기소개서 생성 |
| 커뮤니티 | 게시글과 댓글을 통한 취업 정보 공유 |

## 기술 구성

| 구분 | 기술 |
| --- | --- |
| Backend | Python, Django 4.2 |
| Authentication | Django Auth, django-allauth |
| Database | SQLite |
| Frontend | Django Template, Tailwind CSS, JavaScript |
| AI | SSAFY GMS OpenAI 호환 API |
| 채용 데이터 | 자체 샘플 데이터, 고용24 OpenAPI(사용 권한이 있는 경우) |
| 외부 정보 수집 | Requests, Beautiful Soup |

프로젝트는 기능별로 `accounts`, `jobs`, `resumes`, `community` 앱을 분리했습니다. Django 프로젝트 패키지는 `jasoseo_mate`입니다.

## 실행 방법

```bash
py -3.12 -m venv venv
```

가상환경을 활성화한 뒤 다음 명령을 실행합니다.

이 프로젝트는 Django 4.2의 공식 지원 범위에 맞춰 Python 3.12를 사용합니다. 저장소의 `.python-version`도 3.12로 고정되어 있으며 Python 3.13 이상은 지원하지 않습니다. macOS/Linux에서는 `python3.12 -m venv venv`를 사용하세요.

```bash
pip install -r requirements.txt
```

코드 포맷과 정적 검사를 함께 실행하려면 개발용 의존성을 설치합니다.

```bash
pip install -r requirements-dev.txt
ruff check .
black --check .
djlint --check templates accounts/templates community/templates jobs/templates resumes/templates
```

`.env.example`을 `.env`로 복사하고 필요한 API 키를 설정합니다.

```dotenv
DJANGO_SECRET_KEY=replace-with-a-long-random-secret
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
GMSKEY=
WORKNET_API_KEY=
```

데이터베이스를 준비하고 개발 서버를 실행합니다.

```bash
python manage.py migrate
python manage.py seed_demo_data
python manage.py runserver
```

`seed_demo_data`는 프로필과 매칭에 필요한 스킬 30개와 가상 채용 공고 20개를 생성합니다. 여러 번 실행해도 중복되지 않으며, 모든 샘플 공고는 화면과 데이터베이스에서 실제 공고와 구분됩니다. 샘플 공고만 삭제하려면 다음 명령을 사용합니다.

```bash
python manage.py seed_demo_data --clear
```

서비스는 `http://127.0.0.1:8000/`에서 확인할 수 있습니다. 샘플 데이터와 기본 기능에는 고용24 키가 필요하지 않으며, AI 기능을 사용하려면 `GMSKEY`가 필요합니다.

고용24 OpenAPI는 사용 권한이 있는 기관·기업 환경을 위한 선택 기능입니다. 권한과 `WORKNET_API_KEY`가 있는 경우에만 아래 커맨드를 CLI 또는 cron 작업으로 실행합니다. API 실패 시 샘플이나 스크래핑 데이터로 몰래 대체하지 않습니다.

```bash
python manage.py fetch_worknet_jobs
```

## 운영 전 확인

운영용 비밀 키는 저장소의 예시 값을 복사하지 말고 다음 명령으로 새로 생성해 `DJANGO_SECRET_KEY`에 설정합니다.

```bash
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"
```

운영에서는 `DJANGO_DEBUG=False`, 실제 호스트를 `DJANGO_ALLOWED_HOSTS`에 설정하고 배포 전에 `python manage.py collectstatic --noinput`을 실행합니다. 리버스 프록시가 `X-Forwarded-Proto`를 올바르게 덮어쓰는 환경에서만 `DJANGO_TRUST_PROXY_HEADERS=True`를 사용하고, 서비스의 HTTPS origin을 `DJANGO_CSRF_TRUSTED_ORIGINS`에 쉼표로 구분해 지정합니다. HTTPS 보안 쿠키, 리다이렉트와 HSTS는 DEBUG가 꺼지면 자동 활성화됩니다.

운영 환경에서 이메일 백엔드를 SMTP로 변경한다면 `DJANGO_EMAIL_HOST`, `DJANGO_EMAIL_PORT`, `DJANGO_EMAIL_HOST_USER`, `DJANGO_EMAIL_HOST_PASSWORD`, `DJANGO_EMAIL_USE_TLS`, `DJANGO_DEFAULT_FROM_EMAIL`도 함께 설정해야 합니다. `ACCOUNT_EMAIL_VERIFICATION`의 기본값은 `optional`이므로 비밀번호 재설정과 이메일 인증 과정에서 실제 메일이 발송됩니다.

현재 UI는 별도 Node.js 빌드 과정 없이 실행할 수 있도록 Tailwind CDN을 사용합니다. 정식 대규모 운영 전에는 Tailwind CLI 빌드 결과를 정적 파일로 전환하는 것을 권장합니다.

## 테스트

```bash
python manage.py test
```

현재 테스트는 사용자 데이터 소유권, POST 전용 변경 요청, 샘플 데이터의 중복 방지와 출처 구분, 고용24 공고 동기화 커맨드, 입력값 검증, AI 자기소개서와 실제 공고 데이터의 분리를 확인합니다.

## 프로젝트 상태

현재 버전은 로컬 개발과 기능 시연을 위한 Django 기반 웹 애플리케이션입니다. 운영 배포 시에는 운영용 데이터베이스, 정적 파일 빌드, HTTPS와 배포 서버 구성이 추가로 필요합니다.
