SHELL := /bin/bash
PYTHON := .venv/bin/python
NPM := npm
PORT ?= 8000
E2E_PORT ?= 4321

.PHONY: help setup model workbook site screenshot test test-python test-js test-e2e check verify all serve clean

help:
	@echo "Cafetería Aurora — comandos"
	@echo "  make setup      crea .venv e instala dependencias Python y Node"
	@echo "  make model      regenera data/expected.json desde data/model.json"
	@echo "  make workbook   regenera docs/assets/Cafeteria-Aurora-Modelo-Financiero.xlsx"
	@echo "  make site       construye el sitio en docs/"
	@echo "  make screenshot captura el dashboard en docs/assets/screenshot-dashboard.png"
	@echo "  make test       modelo + libro + sitio + tests Python, Node y navegador"
	@echo "  make check      test + verificación semántica de artefactos"
	@echo "  make all        model + workbook + site + test"
	@echo "  make serve      sirve docs/ en http://localhost:$(PORT)"

setup: .venv node_modules
	@echo "Listo. Ejecuta 'make all' para regenerar y testear."

.venv: requirements.txt
	python3 -m venv .venv
	$(PYTHON) -m pip install --upgrade pip
	$(PYTHON) -m pip install -r requirements.txt
	@touch .venv

node_modules: package.json
	$(NPM) install
	@touch node_modules

model: .venv
	$(PYTHON) scripts/model.py --write

workbook: .venv data/expected.json
	$(PYTHON) scripts/build_workbook.py

site: .venv data/expected.json
	$(PYTHON) scripts/build_site.py

screenshot: node_modules site
	$(PYTHON) scripts/make_screenshot.py

test: model workbook site
	$(MAKE) test-python
	$(MAKE) test-js
	$(MAKE) test-e2e

test-python: .venv
	$(PYTHON) -m pytest

test-js: node_modules
	$(NPM) run test:node

test-e2e: node_modules site
	$(NPM) run test:e2e

check: verify test

verify: .venv
	$(PYTHON) scripts/verify_artifacts.py
	$(PYTHON) scripts/check_links.py

all: model workbook site
	$(MAKE) test-python
	$(MAKE) test-js
	$(MAKE) test-e2e

serve: site
	$(PYTHON) -m http.server $(PORT) --directory docs

clean:
	rm -rf .pytest_cache tests/__pycache__ scripts/__pycache__ node_modules/.cache
