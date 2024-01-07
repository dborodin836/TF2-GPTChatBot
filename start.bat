@echo off
@rem check if venv folder exists, if not, install.
if exist venv (
  call "venv/scripts/activate"
) else (
  call python one_click.py
)
py main.py
