@echo off
setlocal enabledelayedexpansion
@rem check if venv folder exists, if not, install.
set "VENV=%cd%/.venv"
if exist !VENV! (
  call ".venv/scripts/activate" || ( echo. && echo Failed to activate Virtual Environment. Try deleting venv folder and launch start_windows.bat again. && goto end )
) else (
  echo "Virtual Environment (.venv) folder was not found, trying to create it, please wait."
  call python one_click.py
  goto :eof
)
py main.py

:end
pause