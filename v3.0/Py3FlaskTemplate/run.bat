COLOR 0A
ECHO OFF
CLS
echo [DEBUG]: Script has Started.
ECHO [DEBUG]: Checking for Python installation.
for /f "delims=" %%a in ('where.exe python') do (
	@set progpath=%%a
	goto break
)
:break
IF [%progpath%] == [] GOTO MissingPythonError
echo [DEBUG]: Python Program Path: %progpath%
%progpath% --version >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
	ECHO [DEBUG]: Python is probably installed at path.
)
ECHO Setting up and activating venv.
python3 -m venv .venv
call .venv/Scripts/activate
ECHO [DEBUG]: Updating/Installing Pip packages.
for %%r in ("pip" "flask" "flask_wtf") do (
	echo [DEBUG]: Updating/Installing Pip Package: %%r
	%progpath% -m pip install --upgrade %%r
)
ECHO [DEBUG]: Launching Flask Server.
%progpath% main.py
GOTO STOP
:MissingPythonError
ECHO [ERROR]: Failed to find python installation via where command. Exiting...
:STOP
ECHO [DEBUG]: Script has Stopped.
if [%1]==[] goto WAITEND
if "%~1"=="-np" goto END
if "%~1"=="--nopause" goto END
:WAITEND
PAUSE
:END
