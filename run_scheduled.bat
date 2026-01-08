@echo off
REM AI Job Matcher - Scheduled Mode

echo ========================================
echo   AI Job Matcher - Scheduled Mode
echo ========================================
echo.
echo This will run the job matcher daily at the configured time.
echo Keep this window open to keep the scheduler running.
echo Press Ctrl+C to stop.
echo.

call venv\Scripts\activate.bat

python main.py --schedule
