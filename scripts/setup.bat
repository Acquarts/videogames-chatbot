@echo off
REM Setup script for Videogames Chatbot (Windows)

echo ================================
echo Videogames Chatbot - Setup
echo ================================
echo.

REM Check Python
echo Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found! Please install Python 3.11 or higher
    exit /b 1
)
echo [OK] Python found
echo.

REM Create virtual environment
if not exist "venv" (
    echo Creating virtual environment...
    python -m venv venv
    echo [OK] Virtual environment created
) else (
    echo [OK] Virtual environment already exists
)
echo.

REM Activate virtual environment
echo Activating virtual environment...
call venv\Scripts\activate.bat
echo [OK] Virtual environment activated
echo.

REM Upgrade pip
echo Upgrading pip...
python -m pip install --upgrade pip --quiet
echo [OK] Pip upgraded
echo.

REM Install dependencies
echo Installing dependencies...
pip install -r requirements.txt --quiet
if errorlevel 1 (
    echo [ERROR] Failed to install dependencies
    exit /b 1
)
echo [OK] Dependencies installed
echo.

REM Create .env file
if not exist ".env" (
    echo Creating .env file from template...
    copy .env.example .env >nul
    echo [WARNING] Please edit .env file and add your API keys:
    echo    - ANTHROPIC_API_KEY
    echo    - STEAM_API_KEY
) else (
    echo [OK] .env file already exists
)
echo.

REM Create directories
echo Creating necessary directories...
if not exist "chroma_db" mkdir chroma_db
if not exist "logs" mkdir logs
echo [OK] Directories created
echo.

echo ================================
echo Setup complete!
echo ================================
echo.
echo Next steps:
echo 1. Configure your API keys in .env file
echo 2. Run: python -m uvicorn src.main:app --reload
echo 3. Open: http://localhost:8000/docs
echo.
pause
