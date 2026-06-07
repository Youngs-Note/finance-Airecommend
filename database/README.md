# MySQL 최소 스키마

## 목적

MySQL에는 저장이 허용된 앱 내부 데이터만 저장한다.
금융감독원 API 원문과 정규화 상품 결과는 저장하지 않는다.

현재 스키마:

* `app_users`: 로그인과 회원가입에 필요한 사용자 계정
* `app_metadata`: 앱 내부 설정 또는 메타데이터
* `ai_prompt_versions`: OpenAI 설명 프롬프트 변경 이력

## 적용

Windows 개발 환경은 프로젝트 전용 로컬 MySQL 인스턴스를 사용한다.
데이터 디렉터리는 Git에서 제외되는 `.local/mysql-data/`이다.

MySQL Server `8.4` 설치 후 시작:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-local-mysql.ps1
```

종료:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\stop-local-mysql.ps1
```

처음 구성할 때 다음 스크립트가 무작위 로컬 비밀번호, `finance_ai` 데이터베이스, 앱 계정,
ignored `.env` 파일과 스키마를 준비한다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-local-mysql.ps1
```

로컬 `.env`에서 연결 상태 확인을 활성화한다.

```text
MYSQL_ENABLED=true
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_DATABASE=finance_ai
MYSQL_USER=finance_ai
MYSQL_PASSWORD=
```

서버 실행 후 `GET /api/health/mysql`로 연결 상태를 확인한다.

## 저장 범위

* `app_users`: 로그인과 회원가입에 필요한 사용자 계정
* `app_metadata`: 앱 내부 메타데이터
* `ai_prompt_versions`: OpenAI 설명 프롬프트 변경 이력

금융감독원 API 원문과 정규화 금융상품은 MySQL에 저장하지 않는다.
