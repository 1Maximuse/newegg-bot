@echo off
python --version 2>NUL
if errorlevel 1 goto errorNoPython

set /p Delay=Enter delay in seconds:

if exist env\ (
  CALL env/Scripts/activate.bat
  python neweggbot.py %Delay%
) else (
  echo.
  echo First run, installing libraries...
  python -m venv env
  CALL env/Scripts/activate.bat
  python -m pip install -r requirements.txt
  python neweggbot.py %Delay%
)

goto eof

:errorNoPython
echo.
echo Error^: Python is not installed, please install python.

:eof
pause