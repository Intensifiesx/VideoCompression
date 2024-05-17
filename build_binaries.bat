@echo off

REM Create and activate virtual environment
if not exist "venv" (
    python -m venv venv
    cd venv\Scripts
    call "activate"

    REM Install dependencies
    pip install -r ../../requirements.txt

    echo Virtual environment and dependencies set up successfully.
    echo Run the program again to setup the input and output folders.
    pause
    exit /b
)
cd venv\Scripts
call "activate"

pyinstaller -F --icon="../../icon.ico" --distpath "../../dist" --workpath "../../build" "../../Compress.py"
pause
