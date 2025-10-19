# PowerShell script to create Windows Task Scheduler job
# Run this as Administrator: .\setup_windows_task.ps1

$TaskName = "Django-Email-Reports"
$TaskDescription = "Run Django email reports every minute"
$ScriptPath = "python"
$Arguments = "ops\simple_cron.py"
$WorkingDirectory = "C:\Users\fslin\OneDrive\桌面\django learning\minihelper-backend\minihelper_backend"

Write-Host "Setting up Windows Task Scheduler job..." -ForegroundColor Green
Write-Host "Task Name: $TaskName" -ForegroundColor Cyan

try {
    # Check if task already exists
    $ExistingTask = Get-ScheduledTask -TaskName $TaskName -ErrorAction SilentlyContinue
    if ($ExistingTask) {
        Write-Host "Task already exists. Removing old task..." -ForegroundColor Yellow
        Unregister-ScheduledTask -TaskName $TaskName -Confirm:$false
    }

    # Create the action
    $Action = New-ScheduledTaskAction -Execute $ScriptPath -Argument $Arguments -WorkingDirectory $WorkingDirectory

    # Create the trigger (runs every minute)
    $Trigger = New-ScheduledTaskTrigger -Once -At (Get-Date) -RepetitionInterval (New-TimeSpan -Minutes 1) -RepetitionDuration (New-TimeSpan -Days 365)

    # Create the principal (run whether user is logged on or not)
    $Principal = New-ScheduledTaskPrincipal -UserId $env:USERNAME -LogonType Interactive

    # Create the settings
    $Settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable -RunOnlyIfNetworkAvailable

    # Register the task
    Register-ScheduledTask -TaskName $TaskName -Action $Action -Trigger $Trigger -Principal $Principal -Settings $Settings -Description $TaskDescription

    Write-Host "Task '$TaskName' created successfully!" -ForegroundColor Green
    Write-Host "The task will run every minute starting now." -ForegroundColor Green
    Write-Host ""
    Write-Host "To manage the task:" -ForegroundColor Cyan
    Write-Host "- View: Get-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "- Start: Start-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "- Stop: Stop-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White
    Write-Host "- Remove: Unregister-ScheduledTask -TaskName '$TaskName'" -ForegroundColor White

} catch {
    Write-Host "Error creating task: $($_.Exception.Message)" -ForegroundColor Red
    Write-Host "Try running PowerShell as Administrator" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Press any key to continue..."
$null = $Host.UI.RawUI.ReadKey("NoEcho,IncludeKeyDown")