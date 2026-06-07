# 배포 안내

## 추천 배포 구조

이 프로젝트는 다음 구조로 배포한다.

- 프론트엔드: Vercel
- 백엔드 API: Render
- MySQL: Railway MySQL 또는 Aiven MySQL

로컬 MySQL `127.0.0.1:3307`은 개발용이므로 운영 배포에서 사용할 수 없다.

## 배포 순서

1. 외부 MySQL을 먼저 만든다.
2. `database/mysql/schema.sql`을 외부 MySQL에 적용한다.
3. Render에 백엔드 서비스를 만든다.
4. Vercel에 `front/` 프론트엔드 서비스를 만든다.
5. Vercel의 `FASTAPI_BASE_URL`을 Render 백엔드 URL로 설정한다.
6. Vercel의 `NEXTAUTH_URL`을 Vercel 프론트 URL로 설정한다.

## 외부 MySQL

필요한 테이블은 다음 파일에 있다.

```text
database/mysql/schema.sql
```

운영 DB에는 사용자 계정, 앱 메타데이터, AI 프롬프트 버전만 저장한다.
금융감독원 상품 원문과 정규화 결과는 저장하지 않는다.

## Render 백엔드

루트의 `render.yaml`은 Render Blueprint용 설정이다.

빌드 명령:

```bash
python -m pip install --upgrade pip && python -m pip install -r requirements.txt
```

실행 명령:

```bash
uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT
```

필수 환경변수:

```text
APP_ENV=production
APP_DATA_MODE=finlife
FINLIFE_API_KEY=
FINLIFE_BASE_URL=https://finlife.fss.or.kr/finlifeapi
FINLIFE_BANK_GROUP_CODE=020000
FINLIFE_TIMEOUT_SECONDS=10
OPENAI_EXPLANATIONS_ENABLED=false
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4-mini
OPENAI_TIMEOUT_SECONDS=15
MYSQL_ENABLED=true
MYSQL_HOST=
MYSQL_PORT=
MYSQL_DATABASE=
MYSQL_USER=
MYSQL_PASSWORD=
```

OpenAI 크레딧 설정 전에는 `OPENAI_EXPLANATIONS_ENABLED=false`를 유지한다.

Render에서 금융감독원 Finlife API 호출이 실패하면 백엔드는
`backend/app/data/finlife_products.json` 캐시 데이터를 사용한다.
따라서 알파 테스트에서는 `APP_DATA_MODE=finlife`를 유지하되, 상품 API가 실시간 API 또는
캐시 데이터 중 가능한 경로로 응답하는지 확인한다.

## Vercel 프론트엔드

Vercel 프로젝트의 Root Directory는 다음으로 설정한다.

```text
front
```

`front/vercel.json`은 Next.js 빌드 설정을 담는다.

필수 환경변수:

```text
DATABASE_URL=
NEXTAUTH_SECRET=
NEXTAUTH_URL=
FASTAPI_BASE_URL=
```

`DATABASE_URL`은 외부 MySQL 접속 문자열이다.
`FASTAPI_BASE_URL`은 Render 백엔드 URL이다.
`NEXTAUTH_URL`은 Vercel 프론트 URL이다.

예시:

```text
DATABASE_URL=mysql://USER:PASSWORD@HOST:PORT/DATABASE
NEXTAUTH_SECRET=long-random-secret
NEXTAUTH_URL=https://your-front.vercel.app
FASTAPI_BASE_URL=https://your-api.onrender.com
```

## 배포 후 확인

백엔드:

```text
GET https://your-api.onrender.com/api/health
GET https://your-api.onrender.com/api/health/mysql
GET https://your-api.onrender.com/api/products
```

프론트엔드:

```text
https://your-front.vercel.app/login
```

확인 항목:

- 금융감독원 실데이터가 조회되는가
- 지방은행이 노출되지 않는가
- 회원가입과 로그인이 되는가
- 비교 탭 상품 상세가 열리는가
- 추천 결과가 표시되는가

## 주의

- `.env`, `front/.env.local`, API 키, DB 비밀번호는 Git에 올리지 않는다.
- Vercel과 Render의 환경변수는 각 플랫폼 Secret/Environment Variables 화면에서 설정한다.
- 운영 MySQL은 외부에서 접근 가능한 호스트와 포트가 필요하다.
- 무료 플랜 백엔드는 cold start로 첫 응답이 늦을 수 있다.
