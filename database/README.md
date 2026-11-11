# 데이터베이스 (Neon PostgreSQL)

## 목적

DB에는 저장이 허용된 앱 내부 데이터만 저장한다.
금융감독원 API 원문과 정규화 상품 결과는 저장하지 않는다.

현재 스키마 (`database/postgres/schema.sql`):

* `app_users`: 로그인과 회원가입에 필요한 사용자 계정
* `app_metadata`: 앱 내부 설정 또는 메타데이터
* `ai_prompt_versions`: OpenAI 설명 프롬프트 변경 이력

기존 MySQL은 무료 사용 한도 초과로 Neon(서버리스 PostgreSQL)으로 이전했다.
`database/mysql/schema.sql`과 `scripts/*-local-mysql.ps1`은 이전 기록용으로만 남겨 두며
현재 사용하지 않는다.

## Neon 설정

1. <https://neon.tech>에서 프로젝트를 만든다. 데이터베이스 이름은 `finance_ai`를 권장한다.
2. Neon 콘솔 **SQL Editor**에서 `database/postgres/schema.sql` 내용을 실행한다.
   여러 번 실행해도 안전하다(`IF NOT EXISTS`).
3. **Connect** 화면에서 접속 문자열을 복사한다.
4. 루트 `.env`에 백엔드 설정을 넣는다.

   ```text
   DATABASE_ENABLED=true
   DATABASE_URL=postgresql://USER:PASSWORD@ep-xxxx-pooler.REGION.aws.neon.tech/finance_ai?sslmode=require&channel_binding=require
   ```

5. `front/.env.local`에 같은 `DATABASE_URL`을 넣는다.
6. 백엔드 실행 후 `GET /api/health/database`로 연결 상태를 확인한다.

psql이 있다면 2번 대신 다음 명령으로 스키마를 적용할 수 있다.

```bash
psql "$DATABASE_URL" -f database/postgres/schema.sql
```

## 주의

* 스키마는 `schema.sql`로 관리한다. `npx prisma db push`는 Prisma 모델에 없는
  `app_metadata`, `ai_prompt_versions` 테이블을 삭제하려 할 수 있으므로 사용하지 않는다.
* 접속 문자열에는 비밀번호가 포함되므로 `.env`, `.env.local`에만 두고 Git에 올리지 않는다.
* 개발과 운영 데이터를 분리하려면 Neon의 branch 기능으로 개발용 branch를 만든다.

## 저장 범위

* `app_users`: 로그인과 회원가입에 필요한 사용자 계정
* `app_metadata`: 앱 내부 메타데이터
* `ai_prompt_versions`: OpenAI 설명 프롬프트 변경 이력

금융감독원 API 원문과 정규화 금융상품은 DB에 저장하지 않는다.
