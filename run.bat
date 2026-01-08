@echo off
REM AI Job Matcher - Quick Start Script

echo ========================================
echo   AI Job Matcher - Germany Edition
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv\" (
    echo Creating virtual environment...
    python -m venv venv
    echo.
)

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo.

REM Check if dependencies are installed
if not exist "venv\Lib\site-packages\openai\" (
    echo Installing dependencies...
    pip install -r requirements.txt
    echo.
)

REM Check if .env exists
if not exist ".env" (
    echo.
    echo WARNING: .env file not found!
    echo Please copy .env.example to .env and fill in your credentials.
    echo.
    pause
    exit /b 1
)

REM Check if resume exists
if not exist "data\resume.txt" (
    echo.
    echo WARNING: Resume not found at data\resume.txt
    echo Please add your resume before running.
    echo.
    pause
    exit /b 1
)

echo Starting AI Job Matcher...
echo.
python main.py

pause
