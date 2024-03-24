.ONESHELL:

.DEFAULT_GOAL := run

ifeq ($(OS),Windows_NT)

MAKEFILE_LIST = "Makefile"
PYTHON = ".venv/Scripts/python.exe"

define find-functions
	@powershell -Command "$$matches = Select-String -Path $(MAKEFILE_LIST) -Pattern '##'; foreach ($$match in $$matches) { if ($$match.Line -notmatch 'powershell|Select-String') { $$line = $$match.Line; $$line -replace '.*##', '' } }"
endef

help:
	@echo The following commands can be used.
	@echo -----------------------------------
	$(call find-functions)

## run		-	Start electron demo.
run: .venv/Scripts/activate frontend/node_modules
	cd frontend
	npm run demo

## install	-	Install required dependencies (venv, node_modules).
install: .venv/Scripts/activate frontend/node_modules

## build		-	Build whole project to frontend/dist.
build: .venv/Scripts/activate frontend/node_modules
	$(PYTHON) -m PyInstaller -n tf2-gptcb --noconfirm --icon icon.ico -w main.py
	xcopy cfg dist\tf2-gptcb\cfg /E /I /Y
	xcopy icon.png dist\tf2-gptcb /Y
	mkdir dist\tf2-gptcb\logs
	xcopy prompts dist\tf2-gptcb\prompts /E /I /Y

	cd frontend
	npm run pack

## lint		-	Runs linters on src.
lint: .venv/Scripts/activate
	$(PYTHON) -m isort --check-only --profile black .
	$(PYTHON) -m black --check --line-length 100 .

## format		-	Run isort and black on src to automatically fix issues.
format: .venv/Scripts/activate
	$(PYTHON) -m isort --profile black .
	$(PYTHON) -m black --line-length 100 .

# Install .venv for python
.venv/Scripts/activate: requirements.txt
	python -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt

# Install node_modules
frontend/node_modules: frontend/package.json
	cd frontend
	call npm ci

## clean		-	Cleanup.
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

.PHONY: run clean build lint format install