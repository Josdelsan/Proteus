@echo off
setlocal

echo PROTEUS: v1.0.0-aplha.1

@REM Check if Python is installed
python --version >nul 2>&1
if errorlevel 1 (
    echo PROTEUS: Python is not installed on your system.
    echo PROTEUS: Please install Python and try running this script again. Recommended version: 3.10.7
    pause
    exit /b 1
) else (
    echo PROTEUS: Installed Python version
    python --version
)

set "script_dir=%~dp0"
set "venv_dir=%script_dir%proteus_env"

echo PROTEUS: Checking for the existence of virtual environment "proteus_env"
if exist "%venv_dir%" (
    echo PROTEUS: Environment "proteus_env" was found.
) else (
    echo PROTEUS: Environment "proteus_env" was not found.
    echo PROTEUS: Creating a virtual environment...

    python -m venv "%venv_dir%"
    
    if exist "%venv_dir%" (
        echo PROTEUS: Virtual environment created successfully.
    ) else (
        echo PROTEUS: Failed to create the virtual environment.

        @REM If failed to create the venv, show the error message and pause
        pause
        exit /b 1
    )
)

echo PROTEUS: Activating the virtual environment...
call "%venv_dir%\Scripts\activate.bat"

echo PROTEUS: Installing the required packages...
pip install -r "%script_dir%requirements.txt"

@REM Run the application in the background so the console can be closed
echo PROTEUS: Running the application...
start "" /b python -m proteus

endlocal
