@echo off

:: %~dp0 is a built-in variable that expands to the 
:: Drive and Path (D and P) of the current batch file (0).
:: This makes the path to .venv relative to where the batch file is saved.
call "%~dp0\.venv\Scripts\Activate.bat"

:: Execute the Python script. %1 is the full path passed by VS Code.
python -u "%~1"