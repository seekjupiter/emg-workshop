@echo off
setlocal
cd /d "%~dp0"
echo [EMG] Setting up an isolated Python environment...
if not exist "requirements.txt" (
  echo ERROR: requirements.txt not found.
  goto :failed
)
if not exist ".venv\Scripts\python.exe" (
  where py >nul 2>&1
  if not errorlevel 1 (
    py -3.12 --version >nul 2>&1
    if not errorlevel 1 (
      py -3.12 -m venv .venv || goto :failed
    ) else (
      py -3.11 --version >nul 2>&1
      if not errorlevel 1 (
        py -3.11 -m venv .venv || goto :failed
      ) else (
        echo Python 3.11 or 3.12 is required.
        goto :failed
      )
    )
  ) else (
    python --version || goto :failed
    python -m venv .venv || goto :failed
  )
)
".venv\Scripts\python.exe" -m pip install -r requirements.txt || goto :failed
echo.
echo Installation completed. Run 01_Start_EMG_Demo.bat
pause
exit /b 0
:failed
echo.
echo Installation failed. Check Python 3.11/3.12, requirements.txt and network connection.
pause
exit /b 1
