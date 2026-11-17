@echo off
setlocal
cd /d "%~dp0"
echo ==============================================
echo          EPFOSathi - Checkpoint 2 Demo
echo ==============================================
echo.
where python >nul 2>nul
if errorlevel 1 (
  echo ERROR: Python was not found. Install Python 3.10+ and try again.
  pause
  exit /b 1
)
python -c "import streamlit, requests" >nul 2>nul
if errorlevel 1 (
  echo Installing required Python packages...
  python -m pip install -r requirements.txt
  if errorlevel 1 (
    echo.
    echo Dependency installation failed. Check your internet connection and Python/pip setup.
    pause
    exit /b 1
  )
)
echo.
echo Starting the demo backend and Streamlit UI...
echo Keep this window open while using EPFOSathi.
echo Browser: http://localhost:8501
echo Press Ctrl+C in this window to stop the demo.
echo.
python run_demo.py --open-browser
pause
