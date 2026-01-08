@echo off
echo ========================================
echo   AI JOB MATCHER - URGENT MODE
echo ========================================
echo.
echo Running every 30 minutes
echo Finding TOP 10 matches each time
echo Prioritizing urgent/immediate positions
echo.
echo Keep this window open!
echo Press Ctrl+C to stop
echo.
pause

python main.py --schedule
