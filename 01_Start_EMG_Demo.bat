@echo off
setlocal
cd /d "%~dp0"
if not exist ".venv\Scripts\python.exe" (
  echo EMG virtual environment not found.
  echo Run 00_Install.bat first.
  pause
  exit /b 1
)
".venv\Scripts\python.exe" -c "import serial, pyqtgraph, PySide6, numpy" >nul 2>&1
if errorlevel 1 (
  echo Required packages not found.
  echo Run 00_Install.bat first.
  pause
  exit /b 1
)
echo Starting Grove EMG demo...
".venv\Scripts\python.exe" emg_viewer.py
if errorlevel 1 (
  echo.
  echo EMG viewer stopped with an error.
  pause
)
