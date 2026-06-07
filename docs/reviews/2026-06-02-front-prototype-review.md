# 기존 Next.js 프론트엔드 검토

## 결론

`front/`의 UI 골격은 유지하여 사용한다.
다만 현재 상태를 완성된 프론트엔드로 사용하지 않고, FastAPI 백엔드에 맞춰 단계적으로 연결한다.

## 확인한 구조

* Next.js `16.2.3`, React `19.2.4`, TypeScript, Tailwind CSS
* 시작, 로그인, 회원가입, 홈, 상품 목록, 상품 상세, 마이페이지 화면
* NextAuth Credentials 기반 로그인
* Prisma와 SQLite 기반 사용자 및 금융상품 조회
* CSV 파일을 SQLite 금융상품 테이블에 적재하는 기존 시드

## 유지할 부분

* 모바일 앱 형태의 레이아웃
* 시작, 로그인, 회원가입 화면
* 하단 탭 구조
* 상품 목록과 상세 화면의 UI 골격
* 로딩 표시와 검색 입력 UI

## 교체하거나 보완할 부분

### 금융상품 데이터

현재 상품 목록과 상세는 SQLite를 직접 조회한다.
이 흐름은 금융감독원 API를 요청 시점에 조회하고 메모리에서 정규화한다는 현재 정책과 맞지 않는다.

* SQLite 금융상품 조회를 FastAPI `GET /api/products` 호출로 교체한다.
* 상품 상세를 FastAPI `GET /api/products/{product_id}` 호출로 교체한다.
* 숫자형 SQLite ID 대신 백엔드의 문자열 상품 ID를 사용한다.
* CSV 시드와 SQLite 금융상품 테이블은 공식 데이터로 사용하지 않는다.
* 기존 CSV, Excel, SQLite 파일은 Git에 포함하지 않는다.

### 누락 화면

하단 탭과 홈 화면에 `/recommend` 링크가 있지만 대응 페이지가 없다.

* 추천 입력 및 결과 화면을 추가한다.
* FastAPI `POST /api/recommendations`와 연결한다.
* 비교 요약은 `POST /api/products/compare-summary`와 연결한다.
* 금리 차트 화면을 추가한다.

### 사용자 데이터

현재 회원가입과 로그인은 SQLite `User` 테이블을 사용한다.
MySQL을 MVP에서 사용한다는 결정과 맞추려면 사용자 저장 위치를 정해야 한다.

* 사용자 인증을 MVP에 포함할지 확정한다.
* 포함한다면 사용자 테이블을 MySQL로 이전한다.
* 제외한다면 화면은 유지하되 개발 중 인증 우회 또는 비활성 상태를 명시한다.
* 생년월일과 이메일은 개인정보이므로 로컬 DB를 Git에 포함하지 않는다.

### 개발 환경

현재 로컬 PC에는 Node.js가 설치되어 있지 않아 `npm install`, `npm run lint`, `npm run build`를
실행하지 못했다.

Next.js 공식 문서 기준 최소 Node.js 버전은 `20.9`이다.
Prisma 생성물은 Git에서 제외하므로 의존성 설치 후 `npx prisma generate`를 실행해야 한다.

## 발견한 주요 문제

* 로그인 화면이 비밀번호를 브라우저 콘솔에 출력한다.
* 홈 랭킹에 실제 상품처럼 보이는 하드코딩 상품명과 금리가 있다.
* `/recommend` 페이지가 없다.
* 상품 상세는 숫자 ID만 처리하여 FastAPI 문자열 ID와 호환되지 않는다.
* Prisma 생성 절차가 `package.json` 스크립트에 포함되어 있지 않다.
* 기존 SQLite DB에는 사용자 행이 있으므로 공유하거나 커밋하면 안 된다.

## 통합 순서

1. Node.js `20.9` 이상 설치
2. `front/` 의존성 설치와 Prisma Client 생성
3. lint와 build 실행으로 기존 오류 목록 확정
4. 로그인 비밀번호 콘솔 출력 제거
5. 하드코딩 랭킹을 샘플 표시 또는 FastAPI 데이터로 교체
6. 상품 목록과 상세를 FastAPI에 연결
7. 추천 화면과 비교 요약 화면 추가
8. 사용자 인증의 MVP 포함 여부와 MySQL 이전 범위 확정
9. 프론트엔드 실행 문서 갱신

## 검토에 사용한 공식 문서

* Next.js 설치: <https://nextjs.org/docs/app/getting-started/installation>
* Next.js Proxy 규칙: <https://nextjs.org/docs/app/api-reference/file-conventions/proxy>
* Prisma Client 생성: <https://www.prisma.io/docs/orm/prisma-client/setup-and-configuration/generating-prisma-client>

## 2026-06-02 적용 결과

- Node.js LTS `v24.16.0`과 npm `11.13.0`을 설치했습니다.
- Next.js를 `16.2.7`로 갱신하고 `lint`, `build` 검증을 통과했습니다.
- 로그인·회원가입은 로컬 MySQL의 `app_users` 테이블을 사용하도록 전환했습니다.
- 상품 목록·상세·비교 요약·금리 통계·추천 화면은 FastAPI 호출로 전환했습니다.
- 기존 SQLite 마이그레이션은 `front/prisma/migrations-sqlite-legacy/`로 보존했습니다.
- 기존 SQLite DB, CSV, Prisma 생성물은 Git에서 제외했습니다.
