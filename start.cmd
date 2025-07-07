@echo off

title Filelink Server

cd %~dp0
if exist "version\\version.data" (
    for /F "tokens=* usebackq" %%F in (`type version\\version.data`) do (echo Version: %%F)
)

python run.py
if %ERRORLEVEL% == 0 (exit 0) else (
    pause > nul
    exit %ERRORLEVEL%
)