@echo off
REM Batch script to run backend with virtual environment
REM Usage: run_with_venv.bat

echo Activating virtual environment...
call venv\Scripts\activate.bat

if errorlevel 1 (
    echo ERROR: Failed to activate virtual environment
    echo Make sure venv exists. Run: python -m venv venv
    pause
    exit /b 1
)

echo Virtual environment activated.
echo.
echo Starting backend server...
python run.py

pause


