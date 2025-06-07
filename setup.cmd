@echo off

cd %~dp0
echo Setup Filelink...

if not exist requirements.txt (
    echo Create requirements.txt...
    pip freeze > requirements.txt
    if not %ERRORLEVEL% == 0 (goto err)
)

echo Install from requirements.txt...
pip install -r requirements.txt
if not %ERRORLEVEL% == 0 (goto err)

echo.
echo Installation was successful
pause > nul
exit 0

:err
echo.
echo Something went wrong
echo Check python3 and pip3 installed at your machine and try again
pause > nul
exit 1