.ONESHELL:

.DEFAULT_GOAL := run

ifeq ($(OS),Windows_NT)
PYTHON = ".venv/Scripts/python.exe"
CP = xcopy /E /I /Y
EXTRA_PYINSTALLER_FLAGS =

define find-functions
	@powershell -Command "$$matches = Select-String -Path $(MAKEFILE_LIST) -Pattern '##'; foreach ($$match in $$matches) { if ($$match.Line -notmatch 'powershell|Select-String') { $$line = $$match.Line; $$line -replace '.*##', '' } }"
endef

else
PYTHON = ".venv/bin/python3"
CP = cp -r
EXTRA_PYINSTALLER_FLAGS := --hiddenimport 'pkg_resources.extern' --hidden-import='PIL._tkinter_finder'

define find-functions
	@for file in $(MAKEFILE_LIST) ; do \
		grep -E '^##' $$file | grep -v -E 'grep|sed' | sed -E 's/^##//'; \
	done
endef

endif

MAKEFILE_LIST = "Makefile"
BACKEND_NODEMON = "npx nodemon --exec $(PYTHON) main.py --web-server --no-gui"

.PHONY: help
help:
	@echo The following commands can be used.
	@echo -----------------------------------
	$(call find-functions)

## run		-	Start electron demo.
.PHONY: run
run: .venv/pyvenv.cfg frontend/node_modules
	cd frontend
	npm run demo

## dev		-	Start development environment.
.PHONY: dev
dev: .venv/pyvenv.cfg frontend/node_modules
	npx concurrently -k -n "BACK,FRNT" -c "green,yellow" $(BACKEND_NODEMON) "cd frontend && npm run dev"

## install	-	Install required dependencies (venv, node_modules).
.PHONY: install
install: .venv/pyvenv.cfg frontend/node_modules

## build		-	Build whole project to frontend/dist.
.PHONY: build
ifeq ($(OS), Windows_NT)
build: .venv/pyvenv.cfg frontend/node_modules
	$(PYTHON) -m PyInstaller -n tf2-gptcb --noconfirm --icon icon.ico -w $(EXTRA_PYINSTALLER_FLAGS) main.py
	xcopy cfg dist\tf2-gptcb\cfg /E /I /Y
	xcopy icon.png dist\tf2-gptcb /Y
	xcopy commands.yaml dist\tf2-gptcb /Y
	mkdir dist\tf2-gptcb\logs
	xcopy prompts dist\tf2-gptcb\prompts /E /I /Y
	xcopy schemas dist\tf2-gptcb\schemas /E /I /Y

	cd frontend
	npm run pack
else
build: .venv/pyvenv.cfg frontend/node_modules
	$(PYTHON) -m PyInstaller -n tf2-gptcb --noconfirm --icon icon.ico -w $(EXTRA_PYINSTALLER_FLAGS) main.py
	$(CP) cfg dist/tf2-gptcb/cfg
	$(CP) icon.png dist/tf2-gptcb
	$(CP) commands.yaml dist/tf2-gptcb
	mkdir dist/tf2-gptcb/logs
	$(CP) prompts dist/tf2-gptcb/prompts
	$(CP) schemas dist/tf2-gptcb/schemas

	cd frontend
	npm run pack
endif


## lint		-	Runs linters on src.
.PHONY: lint
lint: .venv/pyvenv.cfg
	$(PYTHON) -m isort --check-only .
	$(PYTHON) -m black --check .
	$(PYTHON) -m mypy .

## format		-	Run isort and black on src to automatically fix issues.
.PHONY: format
format: .venv/pyvenv.cfg
	$(PYTHON) -m isort .
	$(PYTHON) -m black .

# Install .venv for python
.venv/pyvenv.cfg: requirements.txt
	python -m venv .venv
	$(PYTHON) -m pip install uv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m uv pip install -r requirements.txt

# Install node_modules
frontend/node_modules: frontend/package.json
	cd frontend && npm ci -d

## clean		-	Cleanup.
.PHONY: clean

TARGETS = \
	.venv \
	.mypy_cache \
	.pytest_cache \
	build \
	dist \
	htmlcov \
	frontend/build \
	frontend/dist \
	frontend/node_modules

ifeq ($(OS), Windows_NT)
	RM = rmdir /s /q
    CLEAN_PATHS = $(subst /,\,$(TARGETS))
    CLEAN_RULE = @for %%d in ($(CLEAN_PATHS)) do @if exist %%d (rd /s /q %%d)
else
	RM = rm -rf
    CLEAN_RULE = $(RM) $(TARGETS)
endif

clean:
	$(CLEAN_RULE)
