set dir=%~dp0
if not exist "%dir%/venv" (
    python -m venv venv
    "%dir%venv\Scripts\python.exe" -m pip install -r "%dir%data\settings\requirements.txt"
)
"%dir%venv\Scripts\python.exe" "%dir%data.py"
pause