# Windows PowerShell 5.1에서도 한글 주석을 읽도록 UTF-8 BOM으로 저장한다.
[CmdletBinding()]
param(
    [switch]$Status,
    [switch]$Pull,
    [switch]$Help,
    [string]$UserHome,
    [string]$CodexHome,
    [string]$PythonExecutable
)

$ErrorActionPreference = 'Stop'

if ($Help) {
    Write-Output 'Usage: sync-gpt.ps1 [-Status | -Pull] [-UserHome PATH] [-CodexHome PATH] [-PythonExecutable PATH]'
    Write-Output 'Default: install managed instructions and skills, then merge declared shared settings.'
    Write-Output '-Status: compare only. -Pull: collect existing managed files and declared settings.'
    exit 0
}
if ($Status -and $Pull) {
    Write-Error '-Status and -Pull cannot be used together.' -ErrorAction Continue
    exit 2
}

try {
    # 명시한 실행 파일을 먼저 사용하고 일반적인 Python 명령을 차례로 확인한다.
    if ($PythonExecutable) {
        $candidates = @([PSCustomObject]@{ Name = $PythonExecutable; Prefix = @() })
    } else {
        $candidates = @(
            [PSCustomObject]@{ Name = 'python'; Prefix = @() },
            [PSCustomObject]@{ Name = 'py'; Prefix = @('-3') },
            [PSCustomObject]@{ Name = 'python3'; Prefix = @() }
        )
    }
    $selectedPython = $null
    $selectedPrefix = @()
    foreach ($candidate in $candidates) {
        $command = Get-Command -Name $candidate.Name -CommandType Application -ErrorAction SilentlyContinue | Select-Object -First 1
        if (-not $command) { continue }
        $prefix = @($candidate.Prefix)
        try {
            & $command.Source @prefix -c 'import sys; sys.exit(0 if sys.version_info >= (3, 11) else 1)' *> $null
            if ($LASTEXITCODE -eq 0) {
                $selectedPython = $command.Source
                $selectedPrefix = $prefix
                break
            }
        } catch {
            continue
        }
    }
    if (-not $selectedPython) {
        throw 'Python 3.11+ was not found. Install Python or pass -PythonExecutable PATH.'
    }

    # 실제 사용자 홈을 변경하지 않고 경로 인자를 공통 엔진에 전달한다.
    $engine = Join-Path $PSScriptRoot 'sync_gpt.py'
    $engineArguments = @('-X', 'utf8', $engine)
    if ($Status) { $engineArguments += '--status' }
    if ($Pull) { $engineArguments += '--pull' }
    if ($UserHome) { $engineArguments += @('--home', $UserHome) }
    if ($CodexHome) { $engineArguments += @('--codex-home', $CodexHome) }
    & $selectedPython @selectedPrefix @engineArguments
    exit $LASTEXITCODE
} catch {
    Write-Error ('ERROR: ' + $_.Exception.Message) -ErrorAction Continue
    exit 2
}
