@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions

REM MagicSquare - create .venv and install dev dependencies
REM Usage: double-click or run from cmd

cd /d "%~dp0"

echo.
echo [MagicSquare] Setting up virtual environment
echo Project: %CD%
echo.

where python >nul 2>&1
if errorlevel 1 (
    echo [ERROR] python not found. Install Python 3.10+ and add to PATH.
    exit /b 1
)

for /f "delims=" %%V in ('python -c "import sys; print(f'{sys.version_info.major}.{sys.version_info.minor}')"') do set PY_VER=%%V
echo [INFO] Python version: %PY_VER%

if not exist ".venv\Scripts\python.exe" (
    echo [INFO] Creating .venv ...
    python -m venv .venv
    if errorlevel 1 (
        echo [ERROR] Failed to create virtual environment.
        exit /b 1
    )
    echo [OK] .venv created
) else (
    echo [INFO] Using existing .venv
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

echo [INFO] Upgrading pip ...
python -m pip install --upgrade pip

echo [INFO] Installing package (editable) and dev dependencies ...
python -m pip install -e ".[dev]"
if errorlevel 1 (
    echo [WARN] Editable install failed. Installing dev packages directly ...
    python -m pip install pytest pytest-cov pytest-mock pydantic black mypy
    if errorlevel 1 (
        echo [ERROR] Package installation failed.
        exit /b 1
    )
)

echo.
echo [OK] Virtual environment is ready.
echo.
echo Next steps:
echo   run_tests.bat
echo   run_tests.bat boundary
echo   run_tests.bat entity
echo   run_tests.bat cov
echo   run_tests.bat cov html
echo.

endlocal
exit /b 0
