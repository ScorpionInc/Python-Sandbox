COLOR 0A
ECHO OFF
CLS
ECHO [DEBUG]: Script has Started.
ECHO [DEBUG]: Checking for Python installation.
FOR /f "delims=" %%a IN ('where.exe python') DO (
	@SET progpath=%%a
	GOTO break
)
:break
IF [%progpath%] == [] GOTO MissingPythonError
ECHO [DEBUG]: Python Program Path: %progpath%
%progpath% --version >NUL 2>&1
IF %ERRORLEVEL% EQU 0 (
	ECHO [DEBUG]: Python is probably installed at this path.
) ELSE (
	GOTO MissingPythonError
)
ECHO [DEBUG]: Setting up and activating venv.
%progpath% -m venv .venv
CALL .venv/Scripts/activate
ECHO [DEBUG]: Updating/Installing Pip packages.
FOR %%r in ("pip" "flask" "flask_wtf") DO (
	ECHO [DEBUG]: Updating/Installing Pip Package: %%r
	REM Using --user doesn't apply as it cant be accessed from virtual environment.
	REM Some warnings were fixed with: --ignore-installed but shouldn't be used each time.
	%progpath% -m pip install --upgrade %%r
)
ECHO [DEBUG]: Launching Flask Server.
%progpath% main.py
GOTO STOP
:MissingPythonError
ECHO [ERROR]: Failed to find python installation via where command. Exiting...
:STOP
ECHO [DEBUG]: Script has Stopped.
IF [%1]==[] GOTO WAITEND
IF "%~1"=="-np" GOTO END
IF "%~1"=="--nopause" GOTO END
:WAITEND
PAUSE
:END
