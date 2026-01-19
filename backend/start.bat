@echo off
REM AI Blog Generator - Quick Start Script for Windows
REM This script helps you get started quickly

echo ========================================
echo AI Blog Generator - Quick Start
echo ========================================
echo.

REM Check if virtual environment exists
if not exist "venv" (
    echo [1/5] Creating virtual environment...
    python -m venv venv
    if errorlevel 1 (
        echo ERROR: Failed to create virtual environment
        pause
        exit /b 1
    )
    echo Virtual environment created!
) else (
    echo [1/5] Virtual environment already exists
)

echo.
echo [2/5] Activating virtual environment...
call venv\Scripts\activate
if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    pause
    exit /b 1
)

echo.
echo [3/5] Installing dependencies...
pip install -r requirements.txt
if errorlevel 1 (
    echo ERROR: Failed to install dependencies
    pause
    exit /b 1
)

echo.
echo [4/5] Checking configuration...
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env
    echo.
    echo IMPORTANT: Edit .env file and add your API keys!
    echo Opening .env file now...
    timeout /t 2 >nul
    notepad .env
) else (
    echo .env file already exists
)

echo.
echo [5/5] Running installation test...
python test_installation.py

echo.
echo ========================================
echo Setup Complete!
echo ========================================
echo.
echo To start the application:
echo.
echo Terminal 1 (Backend):
echo   venv\Scripts\activate
echo   python -m uvicorn app.main:app --reload
echo.
echo Terminal 2 (Frontend):
echo   venv\Scripts\activate
echo   python ui\gradio_app.py
echo.
echo Then open: http://localhost:7860
echo ========================================
echo.
pause
