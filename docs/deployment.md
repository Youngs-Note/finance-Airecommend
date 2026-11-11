# 배포 안내

## 추천 배포 구조

이 프로젝트는 다음 구조로 배포한다.

- 프론트엔드: Vercel
- 백엔드 API: Render
- DB: Neon (서버리스 PostgreSQL)

## 배포 순서

1. Neon 프로젝트를 먼저 만든다.
2. `database/postgres/schema.sql`을 Neon SQL Editor에서 실행한다.
3. Render에 백엔드 서비스를 만든다.
4. Vercel에 `front/` 프론트엔드 서비스를 만든다.
5. Vercel의 `FASTAPI_BASE_URL`을 Render 백엔드 URL로 설정한다.
6. Vercel의 `NEXTAUTH_URL`을 Vercel 프론트 URL로 설정한다.

## Neon 데이터베이스

필요한 테이블은 다음 파일에 있다.

```text
database/postgres/schema.sql
```

Neon 콘솔의 **Connect** 화면에서 접속 문자열을 복사해 `DATABASE_URL`로 사용한다.
Vercel(서버리스)에서는 `-pooler`가 붙은 pooled connection 주소를 권장한다.

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
FINLIFE_CACHE_TTL_SECONDS=21600
OPENAI_EXPLANATIONS_ENABLED=false
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4-mini
OPENAI_TIMEOUT_SECONDS=15
DATABASE_ENABLED=true
DATABASE_URL=
```

OpenAI 크레딧 설정 전에는 `OPENAI_EXPLANATIONS_ENABLED=false`를 유지한다.

Render에서 금융감독원 Finlife API 호출이 실패하면 백엔드는
`backend/app/data/finlife_products.json` 캐시 데이터를 사용한다.
따라서 알파 테스트에서는 `APP_DATA_MODE=finlife`를 유지하되, 상품 API가 실시간 API 또는
캐시 데이터 중 가능한 경로로 응답하는지 확인한다.
`FINLIFE_CACHE_TTL_SECONDS`는 Finlife 상품 조회 메모리 캐시 유지 시간이다.
기본값 `21600`은 6시간을 의미한다.

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

`DATABASE_URL`은 Neon 접속 문자열이다. 백엔드와 같은 값을 사용한다.
`FASTAPI_BASE_URL`은 Render 백엔드 URL이다.
`NEXTAUTH_URL`은 Vercel 프론트 URL이다.

예시:

```text
DATABASE_URL=postgresql://USER:PASSWORD@ep-xxxx-pooler.REGION.aws.neon.tech/finance_ai?sslmode=require&channel_binding=require
NEXTAUTH_SECRET=long-random-secret
NEXTAUTH_URL=https://your-front.vercel.app
FASTAPI_BASE_URL=https://your-api.onrender.com
```

## 배포 후 확인

백엔드:

```text
GET https://your-api.onrender.com/api/health
GET https://your-api.onrender.com/api/health/database
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
- Neon 무료 플랜은 유휴 시 compute가 일시 정지되므로 첫 DB 요청이 몇 초 늦을 수 있다.
- 무료 플랜 백엔드는 cold start로 첫 응답이 늦을 수 있다.
