@echo off
chcp 65001 >nul 2>&1
setlocal EnableExtensions EnableDelayedExpansion

REM MagicSquare - pytest (uses .venv)
REM Usage:
REM   run_tests.bat                  all tests
REM   run_tests.bat boundary         boundary tests only
REM   run_tests.bat entity           user entity tests only
REM   run_tests.bat cov              all tests + coverage (terminal)
REM   run_tests.bat cov html         all tests + coverage + htmlcov/
REM   run_tests.bat cov boundary     boundary + coverage (terminal)
REM   run_tests.bat cov html boundary  boundary + coverage + htmlcov/

cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] .venv not found. Run setup_venv.bat first.
    exit /b 1
)

call ".venv\Scripts\activate.bat"
if errorlevel 1 (
    echo [ERROR] Failed to activate virtual environment.
    exit /b 1
)

set "PYTHONPATH=%CD%"

set "ARG1=%~1"
set "ARG2=%~2"
set "PYTEST_ARGS=tests/ -v"

if /i "%ARG1%"=="boundary" (
    set "PYTEST_ARGS=tests/boundary/ -v"
    goto run
)
if /i "%ARG1%"=="entity" (
    set "PYTEST_ARGS=tests/entity/ -v"
    goto run
)
if /i "%ARG1%"=="cov" (
    if /i "%ARG2%"=="html" (
        if /i "%~3"=="boundary" (
            set "PYTEST_ARGS=tests/boundary/ -v --cov=magic_square/boundary --cov=magic_square/control --cov-report=term-missing --cov-report=html:htmlcov"
        ) else (
            set "PYTEST_ARGS=tests/ -v --cov=magic_square --cov-report=term-missing --cov-report=html:htmlcov"
        )
    ) else if /i "%ARG2%"=="boundary" (
        set "PYTEST_ARGS=tests/boundary/ -v --cov=magic_square/boundary --cov=magic_square/control --cov-report=term-missing"
    ) else (
        set "PYTEST_ARGS=tests/ -v --cov=magic_square --cov-report=term-missing"
    )
    goto run
)

if not "%ARG1%"=="" (
    set "PYTEST_ARGS=tests/ -v %*"
)

:run
echo.
echo [MagicSquare] Running pytest
echo Command: python -m pytest !PYTEST_ARGS!
echo.

python -m pytest !PYTEST_ARGS!
set "EXIT_CODE=!ERRORLEVEL!"

echo.
if "!EXIT_CODE!"=="0" (
    echo [OK] All tests passed.
) else (
    echo [INFO] Some tests failed. This is expected during RED phase.
)

exit /b !EXIT_CODE!
