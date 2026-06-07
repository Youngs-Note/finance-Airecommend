# MVP 구현 순서

## 목적

계획을 실제 개발 순서로 고정합니다. 완료한 항목과 외부 입력이 필요한 항목을 구분합니다.

## 구현 순서

### 1. 공통 환경과 로컬 개발 설정

- [x] `.gitignore`, `.env.example`, `.editorconfig`
- [x] VS Code 권장 확장 설정
- [x] Python 의존성, Ruff, Black
- [x] Node.js LTS `v24.16.0`, npm `11.13.0`

### 2. FastAPI 기반 서버

- [x] 백엔드 패키지 구조와 환경 변수 로딩
- [x] `GET /api/health`, 오류 응답 형식
- [x] 예금·적금 공통 상품 모델
- [x] 상품 목록, 상세, 비교, 통계 API
- [x] 규칙 기반 추천 API

### 3. 금융감독원 API 연동

- [x] API 클라이언트, 페이지네이션, 응답 정규화
- [x] 허용 은행 목록과 인증키 누락 처리
- [x] 제1금융권 허용 정책 목록 작성
- [x] 로컬 보안 입력 스크립트 작성
- [x] 개인 인증키 발급
- [x] 채팅에 노출되지 않은 새 인증키로 교체
- [x] 실제 예금·적금 응답 확인
- [x] 실제 응답의 금융회사명으로 허용 목록 최종 검증

### 4. OpenAI 설명 보조

- [x] OpenAI Responses API 클라이언트와 Structured Outputs 응답 모델
- [x] 추천 설명과 비교 요약 보조
- [x] 실패 시 기본 설명 fallback
- [x] 숫자 주장과 금지 표현 검증
- [x] 실제 OpenAI API 요청과 실패 fallback 확인
- [x] 크레딧 설정 전 로컬 OpenAI 호출 비활성화
- [ ] OpenAI API 결제 또는 크레딧 설정 후 성공 응답 확인

### 5. MySQL과 로그인·회원가입

- [x] 프로젝트 전용 로컬 MySQL 설치와 실행 스크립트
- [x] 메타데이터, AI 프롬프트 버전, `app_users` 스키마
- [x] 로컬 DB 연결 상태 확인
- [x] NextAuth 로그인과 회원가입 연결

### 6. 프론트엔드 통합

- [x] 기존 `front/` Next.js 프로토타입 검토
- [x] 비밀번호 콘솔 출력 제거
- [x] Prisma SQLite 사용자 계정을 MySQL로 전환
- [x] FastAPI 상품 목록과 상세 화면 연결
- [x] 금융감독원 출처와 샘플 데이터 표시
- [x] 추천 입력과 결과 카드 연결
- [x] 비교 요약과 Chart.js 금리 차트 연결
- [ ] UI 세부 개선

## 검증 결과

2026-06-02에 다음 검증을 통과했습니다.

```powershell
.\.venv\Scripts\python.exe -m black --check backend tests
.\.venv\Scripts\python.exe -m ruff check backend tests
.\.venv\Scripts\python.exe -m pytest
.\.venv\Scripts\python.exe -m compileall -q backend
cd front
& "C:\Program Files\nodejs\npm.cmd" run lint
& "C:\Program Files\nodejs\npm.cmd" run build
```

- 백엔드 자동 테스트: `22 passed`
- MySQL health, 상품, 통계, 추천, 비교 요약 API 통합 스모크 테스트 통과
- 프론트 공개 페이지와 인증 보호 리다이렉트 스모크 테스트 통과
- 임시 계정으로 NextAuth 로그인 확인 후 계정 삭제
- 테스트 종료 후 MySQL 사용자 수 `0` 확인

## 다음 외부 조건

- OpenAI API 프로젝트의 결제 또는 사용 가능 크레딧 설정
- OpenAI API 설명 보조 성공 응답 재검증
