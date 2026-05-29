@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions

REM MagicSquare - setup venv then run all tests (one step)

cd /d "%~dp0"

call "%~dp0setup_venv.bat"
if errorlevel 1 exit /b 1

call "%~dp0run_tests.bat"
exit /b %ERRORLEVEL%
