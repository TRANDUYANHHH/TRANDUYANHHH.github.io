@echo off
setlocal
cd /d "%~dp0"
if errorlevel 1 goto failed

set "BLOG_PYTHON="
python -c "import sys; raise SystemExit(sys.version_info < (3, 12))" >nul 2>&1
if not errorlevel 1 set "BLOG_PYTHON=python"
if defined BLOG_PYTHON goto python_ready

py -3 -c "import sys; raise SystemExit(sys.version_info < (3, 12))" >nul 2>&1
if not errorlevel 1 set "BLOG_PYTHON=py -3"
if not defined BLOG_PYTHON goto missing_python

:python_ready
%BLOG_PYTHON% -c "import markdown, pygments" >nul 2>&1
if not errorlevel 1 goto build
echo Installing the required Python libraries...
%BLOG_PYTHON% -m pip install -r requirements.txt
if errorlevel 1 goto failed

:build
echo Building your blog...
%BLOG_PYTHON% scripts\build.py
if errorlevel 1 goto failed
echo.
echo Preview: http://127.0.0.1:4173/
echo Keep this window open. Press Ctrl+C to stop.
%BLOG_PYTHON% scripts\serve.py --open
if errorlevel 1 goto failed
exit /b 0

:missing_python
echo Python 3.12 or newer was not found.
echo Install Python from https://www.python.org/downloads/
echo Then run this file again.
pause
exit /b 1

:failed
echo.
echo Could not start the preview. See the error above and README.md.
echo If port 4173 is in use, close the previous preview and try again.
pause
exit /b 1
