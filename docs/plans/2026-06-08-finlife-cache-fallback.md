# Finlife 캐시 fallback 적용

## 목적

Render 배포 환경에서 금융감독원 Finlife API 호출이 실패할 때도 비교 화면과 AI 추천 화면에 샘플 상품명이 노출되지 않도록 한다.

## 현재 상태

- 로컬에서는 Finlife API 키와 `httpx` 호출이 정상 동작한다.
- Render 백엔드는 `APP_DATA_MODE=finlife`에서 `/api/products`가 502를 반환했다.
- 알파 테스트를 위해 Render 백엔드는 임시로 `APP_DATA_MODE=sample`로 전환되어 있다.
- 이 때문에 프론트의 비교/AI 추천 영역에 `샘플 정액적금 B`, `샘플 자유적금 A` 같은 개발용 데이터가 노출된다.

## 작업 범위

- 로컬에서 공식 Finlife API 응답을 정규화한 캐시 JSON을 생성한다.
- 백엔드가 `finlife` 모드에서 실시간 Finlife API 호출 실패 시 캐시 데이터를 사용하도록 한다.
- 캐시도 없을 때만 기존 오류를 반환한다.
- fallback 동작 테스트를 추가한다.

## 제외 범위

- OpenAI API 실제 호출 연동
- DB에 금융상품을 영구 저장하는 구조 변경
- Render 네트워크 원인 자체의 완전 분석
- 프론트 UI 구조 변경

## 구현 단계

- [x] Finlife 캐시 로더 추가
- [x] 실제 Finlife 상품 캐시 생성
- [x] `ProductService`에 API 실패 시 캐시 fallback 추가
- [x] 테스트 추가 및 실행
- [ ] Render를 다시 `finlife` 모드로 전환 후 배포 검증

## 영향받는 파일 또는 구성 요소

- `backend/app/services/product_service.py`
- `backend/app/data/finlife_cache.py`
- `backend/app/data/finlife_products.json`
- `tests/test_product_service.py`
- `docs/plans/2026-06-08-finlife-cache-fallback.md`

## API / DB / 데이터 변경 사항

- API 응답 형식은 변경하지 않는다.
- DB 스키마 변경은 없다.
- `backend/app/data/finlife_products.json`에 공식 Finlife API 기반 정규화 상품 데이터를 보관한다.

## 검증 방법

- `python -m compileall backend tests`
- `python -m pytest`
- 배포 후 `/api/health`, `/api/products` 확인
- 프론트 비교/AI 추천 화면에서 샘플 상품명이 사라지는지 확인

## 위험 요소 및 확인이 필요한 사항

- 캐시 데이터는 생성 시점 기준이므로 최신 금리와 차이가 날 수 있다.
- Render에서 Finlife API 접근 실패 원인은 별도 분석이 필요하다.
- 캐시 갱신 절차를 문서화하거나 자동화할 필요가 있다.

## 작업 결과

- `backend/app/data/finlife_products.json`에 2026-06-08 기준 공식 Finlife API 기반 상품 32개를 저장했다.
- `ProductService`는 `APP_DATA_MODE=finlife`에서 실시간 API 호출이 실패하면 캐시 상품을 반환한다.
- 캐시 데이터도 없으면 기존처럼 `ExternalApiError`를 반환한다.
- 검증:
  - `python -m compileall backend tests`
  - `python -m pytest`
  - `python -m ruff check backend tests`
  - `python -m black --check backend tests`

남은 작업:

- Render 환경변수를 `APP_DATA_MODE=finlife`로 되돌리고 배포 후 `/api/products` 응답을 확인한다.
