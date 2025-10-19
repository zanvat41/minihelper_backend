@echo off
REM Batch file to create Windows Task Scheduler job
REM Run as Administrator

echo Creating Windows Task Scheduler job for Django email reports...
echo.

REM Delete existing task if it exists
schtasks /delete /tn "Django-Email-Reports" /f >nul 2>&1

REM Create new task
schtasks /create ^
    /tn "Django-Email-Reports" ^
    /tr "python ops\simple_cron.py" ^
    /sc minute ^
    /mo 1 ^
    /sd %date% ^
    /st %time:~0,5% ^
    /f ^
    /ru %username% ^
    /rp ^
    /rl highest

if %errorlevel%==0 (
    echo.
    echo SUCCESS: Task 'Django-Email-Reports' created successfully!
    echo The task will run every minute starting now.
    echo.
    echo To manage the task:
    echo - View all tasks: schtasks /query
    echo - View this task: schtasks /query /tn "Django-Email-Reports"
    echo - Run now: schtasks /run /tn "Django-Email-Reports"
    echo - Stop: schtasks /end /tn "Django-Email-Reports"
    echo - Delete: schtasks /delete /tn "Django-Email-Reports" /f
) else (
    echo ERROR: Failed to create task. Try running as Administrator.
)

echo.
pause