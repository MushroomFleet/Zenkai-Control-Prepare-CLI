@echo off
echo Zenkai Control Prepare - Installation Script
echo ============================================

echo Creating virtual environment...
python -m venv venv

echo Activating virtual environment...
call venv\Scripts\activate.bat

echo Installing dependencies...
pip install -r requirements.txt

echo Installation complete!
echo.
echo To run the application, use run.bat
echo.
pause
