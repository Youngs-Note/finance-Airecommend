# MySQL → Neon(PostgreSQL) 이전

## 목적

기존 외부 MySQL의 무료 사용 한도가 초과되어, 서버리스 PostgreSQL인 Neon으로 DB 환경을 옮긴다.

## 현재 상태

* 백엔드: `pymysql`로 `GET /api/health/mysql` 연결 확인만 수행
* 프론트엔드: Prisma(`provider = "mysql"`) + `@prisma/adapter-mariadb`로 `app_users` 회원가입·로그인
* 스키마: `database/mysql/schema.sql`

## 작업 범위

* 백엔드 DB 드라이버를 `psycopg`로 교체하고 설정을 `DATABASE_ENABLED`, `DATABASE_URL`로 단순화
* 헬스체크 엔드포인트를 `GET /api/health/database`로 변경
* Prisma provider를 `postgresql`, 어댑터를 `@prisma/adapter-pg`로 교체
* PostgreSQL용 `database/postgres/schema.sql` 추가
* `.env.example`, `front/.env.example`, `render.yaml`, 관련 문서 갱신

## 제외 범위

* 기존 MySQL 데이터 이관 (한도 초과로 접근 불가 가능성, 필요 시 별도 작업)
* 로컬 MySQL PowerShell 스크립트와 `database/mysql/schema.sql` 삭제 (이전 기록용으로 보존)

## 구현 단계

- [x] 백엔드 설정·헬스체크·테스트 변경
- [x] PostgreSQL 스키마 작성 (`updated_at` 자동 갱신 트리거 포함)
- [x] Prisma 스키마와 클라이언트 어댑터 변경
- [x] 환경변수 예시, Render 설정, 문서 갱신
- [ ] Neon 프로젝트 생성 및 스키마 적용 (사용자 작업)
- [ ] Render·Vercel 환경변수에 `DATABASE_URL` 등록 (사용자 작업)

## API / DB / 데이터 변경 사항

* `GET /api/health/mysql` 제거 → `GET /api/health/database`
* 환경변수 `MYSQL_*` 제거 → `DATABASE_ENABLED`, `DATABASE_URL`
* `id` 컬럼: `BIGINT UNSIGNED AUTO_INCREMENT` → `BIGSERIAL`
* `ON UPDATE CURRENT_TIMESTAMP` → `set_updated_at()` 트리거

## 검증 방법

* `python -m pytest`, `ruff check .`, `black --check backend tests`
* 로컬 PostgreSQL 16에 `schema.sql` 2회 적용 (재실행 안전성)
* Prisma Client로 `app_users` 생성·수정·조회·중복(P2002)·삭제
* `check_database_connection`으로 실제 연결 성공/실패 확인
* `npx tsc --noEmit`, `npm run lint`, `npm run build`

## 위험 요소 및 확인이 필요한 사항

* `prisma db push`는 Prisma 모델에 없는 테이블을 삭제하려 하므로 사용하지 않는다.
* Neon 무료 플랜은 유휴 시 compute가 정지되어 첫 요청이 느릴 수 있다.
* 실제 Neon 인스턴스 연결은 접속 정보가 없어 이 작업에서 확인하지 못했다.

## 작업 결과

위 검증 항목을 로컬 PostgreSQL 16 기준으로 통과했다. 실제 Neon 연결은 사용자가 접속 문자열을
등록한 뒤 `GET /api/health/database`와 회원가입으로 확인한다.
