# finance-Airecommend

금융감독원 금융상품통합비교공시 Open API에서 예금·적금 상품을 실시간 조회하고,
사용자 조건에 맞는 금융상품을 비교·추천하는 졸업프로젝트입니다.

## 현재 구현 범위

- FastAPI 기반 예금·적금 목록, 상세, 통계, 비교 요약, 규칙 기반 추천 API
- 금융감독원 API 응답 정규화와 제1금융권 허용 목록 필터
- Next.js 기반 로그인·회원가입, 상품 목록·상세·비교, 금리 차트, 추천 화면
- MySQL 기반 사용자 계정, 애플리케이션 메타데이터, AI 프롬프트 버전 저장
- OpenAI Responses API 기반 선택적 설명 보조와 실패 시 기본 설명 fallback
- Ruff, Black, pytest, ESLint, Next.js build 검증

금융상품은 금융감독원 이용 조건에 맞춰 DB나 Git에 복제하지 않습니다.
개발 중에는 직접 작성한 최소 샘플 상품을 사용합니다.

## 최초 환경 준비

Node.js LTS와 MySQL Server가 없다면 설치합니다.

```powershell
winget install --id OpenJS.NodeJS.LTS --exact
winget install --id Oracle.MySQL --exact
```

프로젝트 전용 로컬 MySQL을 최초 1회 설정합니다. 데이터 파일은 Git에서 제외된
`.local/` 아래에 생성되며 `127.0.0.1:3307`을 사용합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup-local-mysql.ps1
```

백엔드와 프론트엔드 의존성을 설치합니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements-dev.txt
cd front
& "C:\Program Files\nodejs\npm.cmd" ci
cd ..
```

PowerShell 실행 정책으로 `npm.ps1` 실행이 차단되면 위 예시처럼 `npm.cmd`를 사용합니다.

## 실행

각 명령은 별도 터미널에서 실행합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\start-local-mysql.ps1
.\.venv\Scripts\python.exe -m uvicorn backend.app.main:app --reload
cd front
& "C:\Program Files\nodejs\npm.cmd" run dev
```

- 프론트엔드: `http://127.0.0.1:3000`
- 백엔드 API 문서: `http://127.0.0.1:8000/docs`

## 금융감독원 API 연결

1. [금융감독원 개인 인증키 신청 화면](https://finlife.fss.or.kr/finlife/api/finlifeApiKey/list.do?menuNo=700034)에서 본인 인증과 이메일 인증을 진행합니다.
2. 사용 목적과 이용 URL을 입력하여 개인 인증키를 발급받습니다.
3. 새 키를 채팅이나 명령어에 직접 붙여넣지 말고 로컬 보안 입력 스크립트로 설정합니다.
4. 실제 응답의 금융회사명을 확인하여 허용 목록을 최종 검증합니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\set-local-api-keys.ps1 -Finlife
```

개인 인증키는 신청 즉시 발급되며, 금융감독원 안내 기준 일일 호출 한도는 10,000건입니다.
자세한 내용은 [금융감독원 API 설정](./docs/setup-finlife-api.md)을 확인합니다.

## OpenAI 설명 보조

추천 순위는 규칙 기반 점수로 결정합니다. OpenAI API는 추천 이유와 비교 요약 문구만
보조하며, 키 누락 또는 호출 실패 시에도 기본 설명을 반환합니다.

```text
OPENAI_EXPLANATIONS_ENABLED=true
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4-mini
```

실제 OpenAI API 요청 도달과 오류 fallback은 확인했습니다.

새 OpenAI API 키를 로컬에 설정할 때는 채팅이나 명령어에 직접 붙여넣지 않고 다음 명령을
실행한 뒤 표시되는 보안 입력란에 붙여넣습니다.

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\set-local-api-keys.ps1 -OpenAI
```

2026-06-02 실제 요청은 OpenAI 서버까지 도달했지만 `429 insufficient_quota`로 fallback 되었습니다.
현재는 로컬 `.env`의 `OPENAI_EXPLANATIONS_ENABLED=false`로 호출을 비활성화하고 규칙 기반
기본 설명을 사용합니다. 추후 결제 또는 사용 가능 크레딧을 설정한 뒤 다시 활성화합니다.

## 검증

```powershell
.\.venv\Scripts\python.exe -m black --check backend tests
.\.venv\Scripts\python.exe -m ruff check backend tests
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q backend
cd front
& "C:\Program Files\nodejs\npm.cmd" run lint
& "C:\Program Files\nodejs\npm.cmd" run build
```

## 문서

- [에이전트 작업 규칙](./AGENTS.md)
- [팀원 GitHub 협업 지침서](./docs/collaboration-guide.md)
- [프로젝트 결정 사항](./docs/project-decisions.md)
- [아키텍처](./docs/architecture.md)
- [API 문서](./docs/api.md)
- [금융감독원 API 인증키 신청](./docs/setup-finlife-api.md)
- [금융상품 데이터 출처와 저장 범위](./docs/data-sources.md)
- [배포 안내](./docs/deployment.md)
- [기존 Next.js 프론트엔드 검토](./docs/reviews/2026-06-02-front-prototype-review.md)
- [프론트엔드 교체 후 연동 검토](./docs/reviews/2026-06-03-front-replacement-review.md)
- [npm 보안 점검](./docs/reviews/2026-06-02-npm-audit.md)
- [실제 API 연동 검증](./docs/reviews/2026-06-02-live-api-validation.md)
- [제한형 알파테스트 검증](./docs/reviews/2026-06-02-alpha-test.md)
- [MVP 구현 순서](./docs/plans/2026-06-02-mvp-implementation-order.md)
- [졸업 프로젝트 계획서](./docs/plans/2026-06-02-graduation-project-plan.md)
- [금융상품 데이터 수집 기능 계획](./docs/plans/2026-06-02-financial-product-data-collection.md)
- [AI API 연동 기능 계획](./docs/plans/2026-06-02-ai-api-integration.md)

졸업 프로젝트 PPT 파일은 GitHub 저장소에 포함하지 않습니다.
