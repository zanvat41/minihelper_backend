@echo off
REM Windows batch file to run cron scheduler every minute
REM This will run the report_by_mail job continuously

echo Starting Django Cron Scheduler...
echo This will run report_by_mail() every minute
echo Press Ctrl+C to stop
echo.

cd /d "%~dp0"

REM Set UTF-8 encoding for console
chcp 65001 > nul

echo Choose an option:
echo 1. Run job once (test)
echo 2. Run continuously (daemon mode)
echo.

choice /c 12 /n /m "Enter choice (1 or 2): "

if errorlevel 2 (
    echo Running in daemon mode...
    python manage.py runcron --daemon
) else (
    echo Running job once...
    python manage.py runcron --once
)

pause