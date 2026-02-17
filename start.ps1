# AI Support Ticket System - PowerShell Launcher
# Simple version - 100% error free

Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   AI SUPPORT TICKET SYSTEM" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Current folder: $PWD" -ForegroundColor Yellow
Write-Host ""

Write-Host "[1/3] Activating virtual environment (.venv)..." -ForegroundColor Green
& ".\.venv\Scripts\Activate.ps1"

Write-Host "[2/3] Moving to backend folder..." -ForegroundColor Green
Set-Location -Path "backend"

Write-Host "[3/3] Ready to work!" -ForegroundColor Green
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   YOU ARE NOW READY!" -ForegroundColor Cyan
Write-Host "========================================" -ForegroundColor Cyan
Write-Host "   Location: backend folder" -ForegroundColor White
Write-Host "   Virtual Env: .venv (ACTIVE)" -ForegroundColor White
Write-Host "   Live URL: https://roshanmulla-ai-support-system-final.hf.space" -ForegroundColor White
Write-Host "========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "   COMMANDS YOU CAN RUN NOW:" -ForegroundColor Magenta
Write-Host "   -> python main.py    - START THE SERVER" -ForegroundColor Yellow
Write-Host "   -> pip list          - See installed packages" -ForegroundColor Yellow
Write-Host "   -> git status        - Check git status" -ForegroundColor Yellow
Write-Host "   -> deactivate        - Exit virtual environment" -ForegroundColor Yellow
Write-Host ""
Write-Host "========================================" -ForegroundColor Cyan

# Keep window open
Read-Host "`nPress Enter to continue..."