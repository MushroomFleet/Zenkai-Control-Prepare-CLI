@echo off
echo Zenkai Control Prepare - Execution Script
echo ========================================

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Running Zenkai Control Prepare...
python main.py

echo.
pause
