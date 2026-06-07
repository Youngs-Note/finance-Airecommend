$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$dataDir = Join-Path $root ".local\mysql-data"
$runDir = Join-Path $root ".local\mysql-run"
$mysqlBaseDir = "C:\Program Files\MySQL\MySQL Server 8.4"
$mysqlBin = Join-Path $mysqlBaseDir "bin"
$mysqld = Join-Path $mysqlBin "mysqld.exe"
$pidFile = Join-Path $runDir "mysql.pid"
$logFile = Join-Path $runDir "mysql.log"

if (-not (Test-Path -LiteralPath $mysqld)) {
    throw "MySQL Server 8.4 is not installed."
}

New-Item -ItemType Directory -Force -Path $dataDir, $runDir | Out-Null

if (-not (Test-Path -LiteralPath (Join-Path $dataDir "mysql"))) {
    & $mysqld --initialize-insecure --basedir="$mysqlBaseDir" --datadir="$dataDir" --log-error="$logFile"
}

if (Test-NetConnection -ComputerName 127.0.0.1 -Port 3307 -InformationLevel Quiet) {
    Write-Output "Local MySQL is already running on 127.0.0.1:3307."
    exit 0
}

Start-Process `
    -FilePath $mysqld `
    -ArgumentList @(
        "--standalone",
        "--bind-address=127.0.0.1",
        "--port=3307",
        "--basedir=`"$mysqlBaseDir`"",
        "--datadir=`"$dataDir`"",
        "--pid-file=`"$pidFile`"",
        "--log-error=`"$logFile`""
    ) `
    -WindowStyle Hidden

for ($attempt = 0; $attempt -lt 30; $attempt++) {
    Start-Sleep -Milliseconds 500
    if (Test-NetConnection -ComputerName 127.0.0.1 -Port 3307 -InformationLevel Quiet) {
        Write-Output "Local MySQL started on 127.0.0.1:3307."
        exit 0
    }
}

throw "Local MySQL did not start. Check $logFile."
