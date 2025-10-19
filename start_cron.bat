@echo off
echo Starting Django Windows Scheduler...
echo.
echo This will run report_by_mail every minute
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"
python manage.py runcron --daemon

pause