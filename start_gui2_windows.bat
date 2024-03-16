@echo off
setlocal enabledelayedexpansion

@rem check if venv folder exists, if not, install.
set "VENV=%cd%/.venv"
if exist !VENV! (
  call ".venv/scripts/activate" || ( echo. && echo Failed to activate Virtual Environment. Try deleting .venv folder and launch start_windows.bat again. && goto end )
) else (
  echo "Virtual Environment (.venv) folder was not found, trying to create it, please wait..."
  py -m venv .venv
  call .venv/scripts/activate
  pip install -r requirements.txt
)

@rem installing node_modules
cd frontend
set "NODE_MODULES=%cd%/node_modules"
if not exist !NODE_MODULES! (
  echo node_modules folder was not found, trying to create it, please wait...
  call npm install
)

@rem start electron
npm run demo

:end
pause