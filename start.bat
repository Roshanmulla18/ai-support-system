@echo off
title AI SUPPORT TICKET SYSTEM
color 0A
cls

echo ╔════════════════════════════════════════════════════════╗
echo ║     🚀 AI SUPPORT TICKET SYSTEM - LAUNCHER            ║
echo ╚════════════════════════════════════════════════════════╝
echo.

:: Step 1: Show current folder
echo 📍 Current folder: %CD%
echo.

:: Step 2: Activate virtual environment
echo 📦 [1/3] Activating virtual environment (.venv)...
call ".\.venv\Scripts\activate.bat"

:: Step 3: Go to backend folder
echo 📂 [2/3] Moving to backend folder...
cd backend

:: Step 4: Show success
echo ✅ [3/3] Ready to work!
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  🎯 YOU ARE NOW READY!                                ║
echo ╠════════════════════════════════════════════════════════╣
echo ║  📍 Location: backend folder                          ║
echo ║  🔧 Virtual Env: .venv (ACTIVE)                       ║
echo ║  🌐 Live URL: roshanmulla-ai-support-system-final.hf.space ║
echo ╚════════════════════════════════════════════════════════╝
echo.
echo ╔════════════════════════════════════════════════════════╗
echo ║  🚀 COMMANDS:                                         ║
echo ╠════════════════════════════════════════════════════════╣
echo ║  ▶ python main.py    - START SERVER                   ║
echo ║  ▶ pip list          - See packages                   ║
echo ║  ▶ deactivate        - Exit venv                      ║
echo ╚════════════════════════════════════════════════════════╝
echo.

cmd /k