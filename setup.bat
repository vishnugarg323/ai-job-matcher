@echo off
echo ========================================
echo   AI JOB MATCHER - URGENT SETUP
echo ========================================
echo.
echo URGENT: Visa expires in 2 months!
echo This tool will find jobs every 30 minutes.
echo.
pause

echo.
echo Step 1: Installing dependencies...
pip install -r requirements.txt

echo.
echo Step 2: Running interactive setup...
python setup.py

echo.
echo ========================================
echo   SETUP COMPLETE!
echo ========================================
echo.
echo NEXT: Add your resume as PDF to data\resume.pdf
echo.
echo Then run: run_urgent.bat
echo.
pause
