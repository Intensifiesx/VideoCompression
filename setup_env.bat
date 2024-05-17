@echo off

REM Create and activate virtual environment
python -m venv venv
call venv\Scripts\activate

REM Install dependencies
pip install -r requirements.txt

echo Virtual environment and dependencies set up successfully.
pause
