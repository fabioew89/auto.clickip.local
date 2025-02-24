# Path to the virtual environment
VENV=.venv
PYTHON=$(VENV)/bin/python
PIP=$(VENV)/bin/pip

# Create the virtual environment
.PHONY: venv
venv:
	@python3 -m venv $(VENV)  # Creates a virtual environment in the specified directory
	@echo "Virtual environment created in $(VENV)"
	@$(PIP) install --upgrade pip > /dev/null  # Upgrades pip inside the virtual environment
	@echo "Pip updated."

# Install dependencies using the virtual environment
.PHONY: install
install: venv
	@$(PIP) install -r requirements.txt > /dev/null  # Installs all dependencies listed in requirements.txt
	@echo "Dependencies installed."

# Run the application using the virtual environment
.PHONY: run
run: venv install
	@$(PYTHON) -m flask --app run.py run --debug  # Runs the Flask application in debug mode
	@echo "Application is running."

# Clean up unnecessary files and caches
.PHONY: clean
clean:
	@find . -type d -name "__pycache__" -exec rm -rf {} +  # Removes Python cache directories
	@find . -type d -name ".pytest_cache" -exec rm -rf {} +  # Removes pytest cache directories
	@echo "Cache successfully removed."

# Run flake8 to check code style, excluding the virtual environment directory
.PHONY: flake
flake:
	@echo 'Checking flake8...'
	@flake8 --exclude $(VENV)  # Runs flake8 while excluding the virtual environment directory
