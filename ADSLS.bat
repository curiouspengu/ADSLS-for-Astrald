set dir=%~dp0
if not exist "%dir%/venv" (
    python -m venv venv
    call "%dir%venv\Scripts\activate.bat"
    pip install -r "%dir%requirements.txt"
)
call "%dir%venv\Scripts\activate.bat"
call "%dir%venv\Scripts\python.exe" "%dir%data.py"