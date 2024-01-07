@echo off
@rem check if venv folder exists, if not, install.
set venv = %cd%/venv
if exist %venv% (
  call "venv/scripts/activate"
) else (
  call python one_click.py
)
py main.py