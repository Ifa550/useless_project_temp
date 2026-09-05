# PowerShell launcher for ICECREAM OS
$Host.UI.RawUI.WindowTitle = "ICECREAM OS - Intelligent Cream Recommendation and Quantity Engine"

$pyPath = "$env:LOCALAPPDATA\Python\pythoncore-3.14-64\python.exe"
if (-not (Test-Path $pyPath)) {
    $pyPath = (Get-Command python -ErrorAction SilentlyContinue).Source
}

if (-not $pyPath) {
    Write-Host "[ERROR] Python was not detected at $pyPath" -ForegroundColor Red
    Pause
    exit 1
}

Write-Host "========================================================" -ForegroundColor Cyan
Write-Host " ICECREAM OS: Launching Mission Control Telemetry...     " -ForegroundColor Cyan
Write-Host "========================================================" -ForegroundColor Cyan

& "$pyPath" "$PSScriptRoot\main.py"
