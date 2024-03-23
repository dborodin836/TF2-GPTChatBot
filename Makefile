.ONESHELL:

.DEFAULT_GOAL := run

ifeq ($(OS),Windows_NT)

PYTHON = ".venv/Scripts/python.exe"

run: .venv/Scripts/activate frontend/node_modules
	cd frontend
	npm run demo

install: .venv/Scripts/activate frontend/node_modules

build: .venv/Scripts/activate frontend/node_modules
	$(PYTHON) -m PyInstaller -n tf2-gptcb --noconfirm --icon icon.ico -w main.py
	xcopy cfg dist\tf2-gptcb\cfg /E /I /Y
	xcopy icon.png dist\tf2-gptcb /Y
	mkdir dist\tf2-gptcb\logs
	xcopy prompts dist\tf2-gptcb\prompts /E /I /Y

	cd frontend
	npm run pack

.venv/Scripts/activate: requirements.txt
	python -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

frontend/node_modules: frontend/package.json
	cd frontend
	call npm ci

clean:
	if exist ".venv" (rd /s /q ".venv")
	if exist "build" (rd /s /q "build")
	if exist "dist" (rd /s /q "dist")
	if exist "htmlcov" (rd /s /q "htmlcov")
	if exist "frontend/build" (rd /s /q "frontend/build")
	if exist "frontend/dist" (rd /s /q "frontend/dist")
	if exist "frontend/node_modules" (rd /s /q "frontend/node_modules")

else
endif

.PHONY: run clean build