$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$pidFile = Join-Path $root ".local\mysql-run\mysql.pid"

if (-not (Test-Path -LiteralPath $pidFile)) {
    Write-Output "Local MySQL PID file was not found."
    exit 0
}

$processId = [int](Get-Content -LiteralPath $pidFile)
$process = Get-Process -Id $processId -ErrorAction SilentlyContinue
if ($null -eq $process) {
    Write-Output "Local MySQL is not running."
    exit 0
}

Stop-Process -Id $processId
Write-Output "Local MySQL stopped."
