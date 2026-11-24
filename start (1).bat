@echo off
cd /d "%~dp0"
title HeadCount AI
echo Folder: %CD%
echo.

if not exist run.py goto norun

set PY=
where py >nul 2>nul && set PY=py -3
if not defined PY where python >nul 2>nul && set PY=python
if not defined PY goto nopython

if not exist backend\models mkdir backend\models
if exist backend\models\face_detection_yunet_2026may.onnx goto modelok
if exist src\face_detection_yunet_2026may.onnx copy src\face_detection_yunet_2026may.onnx backend\models\ >nul
if not exist backend\models\face_detection_yunet_2026may.onnx goto nomodel
:modelok
echo [1/3] Model mil gaya.

if exist venv\Scripts\python.exe goto venvok
echo [2/3] Virtual environment ban raha hai...
%PY% -m venv venv
if errorlevel 1 goto venvfail
:venvok

if exist venv\.installed goto start
echo [3/3] Libraries install ho rahi hain, 2-3 minute lagenge...
venv\Scripts\python.exe -m pip install -r backend\requirements.txt
if errorlevel 1 goto pipfail
echo ok> venv\.installed

:start
echo.
echo Server chalu ho raha hai. Is window ko band mat karo.
start "" cmd /c "ping 127.0.0.1 -n 6 >nul & start http://127.0.0.1:5000/dashboard.html"
venv\Scripts\python.exe run.py
echo.
echo Server ruk gaya. Upar ka error message padho.
pause
exit /b 0

:norun
echo ERROR: run.py nahi mili. start.bat ko HeadCountDetection folder ke andar rakho.
pause
exit /b 1

:nopython
echo ERROR: Python nahi mila. python.org se install karo aur "Add Python to PATH" tick karo.
pause
exit /b 1

:nomodel
echo ERROR: face_detection_yunet_2026may.onnx nahi mila. Isse backend\models folder me rakho.
pause
exit /b 1

:venvfail
echo ERROR: Virtual environment nahi ban paya. Folder venv delete karke dobara chalao.
pause
exit /b 1

:pipfail
echo ERROR: Libraries install nahi hui. Internet check karo aur dobara chalao.
pause
exit /b 1
