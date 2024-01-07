@rem TODO: One-click installer.
set VENV_DIR=%cd%\venv

if not exist %VENV_DIR% (
	py -m venv venv || ( echo. && echo Failed to create venv. && goto end )
	py -m pip install -r requirements.txt || ( echo. && echo Failed to install requirements. && goto end )
)

call "venv\scripts\activate"
py main.py