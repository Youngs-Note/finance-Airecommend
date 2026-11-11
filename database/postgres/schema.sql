-- Neon(PostgreSQL)용 앱 내부 데이터 스키마
-- 금융감독원 API 원문과 정규화 금융상품은 저장하지 않는다.

-- MySQL의 ON UPDATE CURRENT_TIMESTAMP를 대신하는 트리거 함수
CREATE OR REPLACE FUNCTION set_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TABLE IF NOT EXISTS app_metadata (
    metadata_key VARCHAR(100) PRIMARY KEY,
    metadata_value TEXT NOT NULL,
    updated_at TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS ai_prompt_versions (
    id BIGSERIAL PRIMARY KEY,
    feature_name VARCHAR(100) NOT NULL,
    prompt_version VARCHAR(50) NOT NULL,
    model_name VARCHAR(100) NOT NULL,
    instructions TEXT NOT NULL,
    is_active BOOLEAN NOT NULL DEFAULT FALSE,
    created_at TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_ai_prompt_versions_feature_version UNIQUE (feature_name, prompt_version)
);

CREATE TABLE IF NOT EXISTS app_users (
    id BIGSERIAL PRIMARY KEY,
    user_id VARCHAR(100) NOT NULL,
    email VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    name VARCHAR(100) NOT NULL,
    birth DATE NOT NULL,
    created_at TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT uq_app_users_user_id UNIQUE (user_id),
    CONSTRAINT uq_app_users_email UNIQUE (email)
);

DROP TRIGGER IF EXISTS trg_app_metadata_updated_at ON app_metadata;
CREATE TRIGGER trg_app_metadata_updated_at
    BEFORE UPDATE ON app_metadata
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();

DROP TRIGGER IF EXISTS trg_app_users_updated_at ON app_users;
CREATE TRIGGER trg_app_users_updated_at
    BEFORE UPDATE ON app_users
    FOR EACH ROW EXECUTE FUNCTION set_updated_at();
