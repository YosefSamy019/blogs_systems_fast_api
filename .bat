@echo off
REM -----------------------------------------
REM Activate the virtual environment
REM -----------------------------------------
call D:\AI\Projects\APIs\blogs_systems_fast_api\.venv\Scripts\activate.bat

REM -----------------------------------------
REM Upgrade pip first
REM -----------------------------------------
python -m pip install --upgrade pip

REM -----------------------------------------
REM Install essential packages only
REM -----------------------------------------


pip install fastapi
pip install uvicorn


REM -----------------------------------------
REM Done
REM -----------------------------------------
echo All essential packages installed successfully!
pause
