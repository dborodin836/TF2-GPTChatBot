@echo off
setlocal enabledelayedexpansion
@rem check if venv folder exists, if not, install.
set "VENV=%cd%/venv"
if exist !VENV! (
  call "venv/scripts/activate"
) else (
  call python one_click.py
  goto :eof
)
py main.py
