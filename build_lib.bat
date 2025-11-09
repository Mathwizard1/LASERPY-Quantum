@echo off

:: Change directory to the location of the batch file
cd "%~dp0"

:: Check if the 'dist' folder exists
if exist "dist" (
    echo Deleting 'dist' folder...
    :: The /S switch means delete all files and subfolders in 'dist'
    :: The /Q switch means quiet mode (no confirmation prompt)
    rmdir /s /q "dist"
    echo 'dist' folder deleted successfully.
) else (
    echo 'dist' folder not found. Nothing to delete.
)

:: The FOR /D command iterates over directories (folders) that match the wildcard pattern.
:: %%i is the loop variable for the directory name.
FOR /D %%i IN (*.egg-info) DO (
    echo Deleting "%%i"...
    rmdir /s /q "%%i"
)

:: Execute the build command. 
call ".\.venv\Scripts\Activate.bat"
python -m build