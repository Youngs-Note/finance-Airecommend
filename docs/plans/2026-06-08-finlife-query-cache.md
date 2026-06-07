# Finlife 상품 조회 캐싱

## 목적

금융상품 조회 시 매 요청마다 금융감독원 Finlife API를 호출하지 않도록 TTL 메모리 캐시를 추가한다.
응답 속도를 개선하고 외부 API 장애 또는 지연에 대한 안정성을 높인다.

## 현재 상태

- `APP_DATA_MODE=finlife`에서는 상품 조회마다 Finlife API를 호출한다.
- Render 배포 환경에서는 Finlife API 실시간 호출이 실패할 수 있어 정적 JSON fallback을 사용한다.
- 현재 fallback은 장애 대응용이며, 정상 상황의 반복 조회 비용을 줄이는 TTL 캐시는 없다.

## 작업 범위

- Finlife 상품 목록에 대한 프로세스 메모리 TTL 캐시를 추가한다.
- 기본 TTL 설정을 환경변수로 관리한다.
- TTL 안에서는 동일 상품 유형 조회가 외부 API를 다시 호출하지 않도록 한다.
- TTL이 만료되면 Finlife API를 다시 호출하고 캐시를 갱신한다.
- Finlife API 실패 시 기존 JSON 캐시 fallback은 유지한다.
- 캐싱 동작 테스트를 추가한다.

## 제외 범위

- MySQL 상품 저장소 구현
- Redis 같은 외부 캐시 도입
- 캐시 강제 갱신 관리자 화면
- 프론트 UI 변경

## 구현 단계

- [x] 캐시 TTL 설정값 추가
- [x] `ProductService`에 상품 유형별 TTL 메모리 캐시 추가
- [x] 캐시 hit, TTL 만료, fallback 동작 테스트 추가
- [x] 테스트 및 린트 실행
- [ ] `develop` 푸시 및 Render 배포 확인

## 영향받는 파일 또는 구성 요소

- `backend/app/core/config.py`
- `backend/app/services/product_service.py`
- `tests/test_product_service.py`
- `docs/deployment.md`
- `docs/plans/2026-06-08-finlife-query-cache.md`

## API / DB / 데이터 변경 사항

- API 응답 형식 변경 없음
- DB 스키마 변경 없음
- 새 환경변수:

```text
FINLIFE_CACHE_TTL_SECONDS=21600
```

## 검증 방법

- `python -m compileall backend tests`
- `python -m pytest`
- `python -m ruff check backend tests`
- `python -m black --check backend tests`
- 배포 후 `/api/health`, `/api/products` 확인

## 위험 요소 및 확인이 필요한 사항

- 캐시 TTL 동안 최신 금리 변경이 즉시 반영되지 않을 수 있다.
- Render 무료 플랜은 서버 재시작 시 메모리 캐시가 사라질 수 있다.
- 여러 인스턴스를 사용할 경우 인스턴스별 캐시가 따로 유지된다.

## 작업 결과

- `FINLIFE_CACHE_TTL_SECONDS` 설정을 추가했다.
- `ProductService`에 프로세스 메모리 기반 Finlife 상품 캐시를 추가했다.
- 캐시는 예금/적금을 함께 갱신하고, 상품 유형별 조회 시 필요한 유형만 반환한다.
- TTL이 만료된 뒤 실시간 Finlife API 호출이 실패하면 마지막 성공 메모리 캐시를 우선 반환한다.
- 마지막 성공 메모리 캐시가 없으면 기존 정적 JSON fallback을 사용한다.
- 검증:
  - `python -m compileall backend tests`
  - `python -m pytest`
  - `python -m ruff check backend tests`
  - `python -m black --check backend tests`

남은 작업:

- `develop`에 푸시하고 Render 배포 후 `/api/products` 응답을 확인한다.
