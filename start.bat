@echo off
title AutoResolve AI - Phase 3
color 0A
cls

echo ========================================================
echo    AUTORESOLVE AI - QUICK LAUNCHER
echo    Phase 3: Authentication System
echo ========================================================
echo.

:: Check for virtual environment
if exist "venv310\" (
    set VENV=venv310
) else if exist "venv\" (
    set VENV=venv
) else (
    echo [ERROR] No virtual environment found!
    echo Run: py -3.10 -m venv venv310
    pause
    exit
)

:: Activate venv
echo [1/3] Activating %VENV%...
call %VENV%\Scripts\activate.bat

:: Go to backend
echo [2/3] Moving to backend folder...
cd backend

:: Ready
echo [3/3] Ready to work!
echo.
echo ========================================================
echo    COMMANDS:
echo    python main.py     - Start server (port 8001)
echo    python test_db.py  - Test database
echo    python backup_db.py - Backup database
echo ========================================================
echo.
echo    URL: http://localhost:8001
echo    Docs: http://localhost:8001/docs
echo ========================================================
echo.

cmd /k