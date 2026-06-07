$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$mysql = "C:\Program Files\MySQL\MySQL Server 8.4\bin\mysql.exe"
$rootPasswordFile = Join-Path $root ".local\mysql-root-password.txt"
$backendEnvFile = Join-Path $root ".env"
$frontendEnvFile = Join-Path $root "front\.env.local"
$schemaFile = Join-Path $root "database\mysql\schema.sql"

if (-not (Test-Path -LiteralPath $mysql)) {
    throw "MySQL Server 8.4 is not installed."
}

if (Test-Path -LiteralPath $rootPasswordFile) {
    throw "Local MySQL is already configured."
}

if ((Test-Path -LiteralPath $backendEnvFile) -or (Test-Path -LiteralPath $frontendEnvFile)) {
    throw "An environment file already exists. Back it up before running the setup script."
}

& (Join-Path $PSScriptRoot "start-local-mysql.ps1")

$appPassword = -join ((1..48) | ForEach-Object { "{0:x}" -f (Get-Random -Maximum 16) })
$rootPassword = -join ((1..48) | ForEach-Object { "{0:x}" -f (Get-Random -Maximum 16) })
$nextAuthSecret = -join ((1..64) | ForEach-Object { "{0:x}" -f (Get-Random -Maximum 16) })

$initializeSql = @"
ALTER USER 'root'@'localhost' IDENTIFIED BY '$rootPassword';
CREATE DATABASE IF NOT EXISTS finance_ai CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
CREATE USER IF NOT EXISTS 'finance_ai'@'%' IDENTIFIED BY '$appPassword';
ALTER USER 'finance_ai'@'%' IDENTIFIED BY '$appPassword';
GRANT ALL PRIVILEGES ON finance_ai.* TO 'finance_ai'@'%';
FLUSH PRIVILEGES;
"@

$initializeSql | & $mysql --protocol=tcp --host=127.0.0.1 --port=3307 --user=root
if ($LASTEXITCODE -ne 0) {
    throw "MySQL account initialization failed."
}

Set-Content -LiteralPath $rootPasswordFile -Value $rootPassword -NoNewline

$backendEnv = @"
APP_NAME=finance-Airecommend API
APP_ENV=development
APP_DATA_MODE=sample
FINLIFE_API_KEY=
FINLIFE_BASE_URL=https://finlife.fss.or.kr/finlifeapi
FINLIFE_BANK_GROUP_CODE=020000
FINLIFE_TIMEOUT_SECONDS=10
OPENAI_EXPLANATIONS_ENABLED=false
OPENAI_API_KEY=
OPENAI_MODEL=gpt-5.4-mini
OPENAI_TIMEOUT_SECONDS=15
MYSQL_ENABLED=true
MYSQL_HOST=127.0.0.1
MYSQL_PORT=3307
MYSQL_DATABASE=finance_ai
MYSQL_USER=finance_ai
MYSQL_PASSWORD=$appPassword
"@
Set-Content -LiteralPath $backendEnvFile -Value $backendEnv

$frontendEnv = @"
DATABASE_URL=mysql://finance_ai:$appPassword@127.0.0.1:3307/finance_ai
NEXTAUTH_SECRET=$nextAuthSecret
NEXTAUTH_URL=http://127.0.0.1:3000
FASTAPI_BASE_URL=http://127.0.0.1:8000
"@
Set-Content -LiteralPath $frontendEnvFile -Value $frontendEnv

$env:MYSQL_PWD = $appPassword
Get-Content -LiteralPath $schemaFile |
    & $mysql --protocol=tcp --host=127.0.0.1 --port=3307 --user=finance_ai finance_ai
Remove-Item Env:MYSQL_PWD

if ($LASTEXITCODE -ne 0) {
    throw "MySQL schema initialization failed."
}

Write-Output "Local MySQL setup is complete."
