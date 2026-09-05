@echo off
setlocal
title ICECREAM OS - Intelligent Cream Recommendation and Quantity Engine

set "PY=C:\Users\user\AppData\Local\Python\pythoncore-3.14-64\python.exe"

if not exist "%PY%" (
    set "PY=python"
)

echo ========================================================
echo  ICECREAM OS: Launching Mission Control Telemetry...
echo ========================================================
"%PY%" "%~dp0main.py"
if %ERRORLEVEL% NEQ 0 (
    echo.
    echo [ERROR] Application exited with code %ERRORLEVEL%.
    pause
)
