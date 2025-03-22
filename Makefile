VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

.PHONY: venv
.PHONY: install
.PHONY: run
.PHONY: clean
.PHONY: flake

venv:
	@python3 -m venv $(VENV)
	@echo "Virtual environment created in $(VENV)"
	@$(PIP) install --upgrade pip > /dev/null
	@echo "Pip updated."

install: venv
	@$(PIP) install -r requirements.txt
	@echo "Dependencies installed."

run:
	@PYTHONDONTWRITEBYTECODE=1 FLASK_ENV=development FLASK_APP=run.py $(PYTHON) -m flask run --debug --reload
	@echo "Application is running."

clean:
	@find . -type d \( -name "__pycache__" -o -name ".pytest_cache" \) -exec rm -rf {} +
	@find . -type f -name "*.pyc" -delete
	@rm -rf $(VENV)
	@echo "Cache and $(VENV) successfully removed."

flake:
	@echo 'Checking flake8...'
	@flake8 --exclude $(VENV)