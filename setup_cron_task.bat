@echo off
REM One-time setup script for Django cron job
REM This will create a Windows Task that runs every minute

echo ================================================================
echo Django Email Reports - Windows Task Setup
echo ================================================================
echo.
echo This will create a Windows Task that runs every minute to send
echo email reports using your Django report_by_mail() function.
echo.

REM Check if running as admin
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo WARNING: Not running as Administrator.
    echo The task may not be created properly.
    echo.
    echo Please right-click this file and "Run as Administrator" for best results.
    echo.
    pause
)

echo Setting up the task...
echo.

REM Get current directory
set "CURRENT_DIR=%~dp0"
set "PYTHON_SCRIPT=%CURRENT_DIR%manage.py"
set "WORK_DIR=%CURRENT_DIR%"

echo Working directory: %WORK_DIR%
echo Django command: python %PYTHON_SCRIPT% runcron --daemon
echo.

REM Delete existing task if it exists
schtasks /delete /tn "Django-Email-Reports" /f >nul 2>&1

REM Create the task to run every minute using Django management command
schtasks /create ^
    /tn "Django-Email-Reports" ^
    /tr "python manage.py runcron --once" ^
    /sc minute ^
    /mo 1 ^
    /sd %date% ^
    /st %time:~0,5% ^
    /ru "%username%" ^
    /f

if %errorlevel%==0 (
    echo.
    echo ✓ SUCCESS! Windows Task created successfully!
    echo.
    echo Task Name: Django-Email-Reports
    echo Frequency: Every 1 minute
    echo Script: %PYTHON_SCRIPT%
    echo.
    echo The task will start automatically and run every minute.
    echo.
    echo Management commands:
    echo - View task: schtasks /query /tn "Django-Email-Reports"
    echo - Run now: schtasks /run /tn "Django-Email-Reports"
    echo - Disable: schtasks /change /tn "Django-Email-Reports" /disable
    echo - Enable: schtasks /change /tn "Django-Email-Reports" /enable
    echo - Delete: schtasks /delete /tn "Django-Email-Reports" /f
    echo.
    echo You can also manage it through Task Scheduler GUI:
    echo Press Win+R, type: taskschd.msc
    echo.
) else (
    echo ❌ ERROR: Failed to create the task.
    echo.
    echo Possible solutions:
    echo 1. Run this script as Administrator
    echo 2. Check if Python is in your PATH
    echo 3. Manually create the task using Task Scheduler GUI
    echo.
)

echo ================================================================
pause