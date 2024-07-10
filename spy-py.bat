@echo off
title spy-py

python --version >nul 2>&1
if errorlevel 1 (
    python3 --version >nul 2>&1
    if errorlevel 1 (
        echo Python is not installed. Please install Python 3.6 or higher.
        pause
        exit /b
    )
)

echo Initializing virtual environment...
python -m venv Spy-Py
call Spy-Py/Scripts/activate 
echo Installing required packages...
pip install -r requirements.txt

cls

python builder.py

echo.
echo ########################################################
echo #                                                      #
echo #  Spy-Py build complete. If you find this project     #
echo #    useful, please consider starring it on GitHub!    #
echo #   Remember to use the software responsibly, and      #
echo #     note that I am not liable for any actions you    #
echo #   choose to take with it. Thanks for using Spy-py!   #
echo #                                                      #
echo ########################################################
echo.
pause
exit /b
