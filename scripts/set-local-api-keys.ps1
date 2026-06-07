param(
    [switch]$Finlife,
    [switch]$OpenAI
)

$ErrorActionPreference = "Stop"

$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root ".env"
$exampleFile = Join-Path $root ".env.example"

if (-not $Finlife -and -not $OpenAI) {
    $Finlife = $true
    $OpenAI = $true
}

if (-not (Test-Path -LiteralPath $envFile)) {
    Copy-Item -LiteralPath $exampleFile -Destination $envFile
}

function Read-SecretValue {
    param([string]$Prompt)

    $secureValue = Read-Host -Prompt $Prompt -AsSecureString
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($secureValue)
    try {
        return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer)
    }
    finally {
        [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer)
    }
}

function Set-EnvValue {
    param(
        [string]$Name,
        [string]$Value
    )

    $lines = @(Get-Content -LiteralPath $envFile -Encoding utf8)
    $pattern = "^{0}=" -f [Regex]::Escape($Name)
    $matched = $false

    $updatedLines = foreach ($line in $lines) {
        if ($line -match $pattern) {
            $matched = $true
            "{0}={1}" -f $Name, $Value
        }
        else {
            $line
        }
    }

    if (-not $matched) {
        $updatedLines += "{0}={1}" -f $Name, $Value
    }

    Set-Content -LiteralPath $envFile -Value $updatedLines -Encoding utf8
}

if ($Finlife) {
    $finlifeKey = Read-SecretValue "New Finlife API key"
    if ([string]::IsNullOrWhiteSpace($finlifeKey)) {
        throw "Finlife API key cannot be empty."
    }

    Set-EnvValue -Name "FINLIFE_API_KEY" -Value $finlifeKey
    Set-EnvValue -Name "APP_DATA_MODE" -Value "finlife"
}

if ($OpenAI) {
    $openAiKey = Read-SecretValue "New OpenAI API key"
    if ([string]::IsNullOrWhiteSpace($openAiKey)) {
        throw "OpenAI API key cannot be empty."
    }

    Set-EnvValue -Name "OPENAI_API_KEY" -Value $openAiKey
    Set-EnvValue -Name "OPENAI_EXPLANATIONS_ENABLED" -Value "true"
}

Write-Output "Local API keys were updated in the ignored .env file."
