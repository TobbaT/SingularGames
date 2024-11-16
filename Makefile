# Define the name of the virtual environment directory
VENV_NAME ?= venv

# Define the command to activate the virtual environment
VENV_ACTIVATE = . $(VENV_NAME)/bin/activate

# Set the Python interpreter to use within the virtual environment
PYTHON = $(VENV_NAME)/bin/python3

# Default target (runs when you just type 'make')
.DEFAULT_GOAL := help

# Help target to display available commands
help:
	@echo "Available commands:"
	@echo "  make setup      - Set up the virtual environment and install dependencies"
	@echo "  make run        - Run the game with the specified file"
	@echo "  make clean      - Clean up generated files and the virtual environment"

# Setup target to create the virtual environment and install dependencies
setup: $(VENV_NAME)/bin/activate
$(VENV_NAME)/bin/activate: setup.sh requirements.txt
	@echo "Creating virtual environment..."
	python3 -m venv $(VENV_NAME)
	@echo "Installing dependencies..."
	$(VENV_ACTIVATE) && pip install -r requirements.txt
	@echo "Sourcing setup.sh..."
	$(VENV_ACTIVATE) && source .env
	touch $(VENV_NAME)/bin/activate

# Run target to execute the game with the specified file
run: setup
	$(VENV_ACTIVATE) && python3 run-game.py -game 'Stacktician.md'

# Clean target to remove generated files and the virtual environment
clean:
	@echo "Cleaning up..."
	rm -rf $(VENV_NAME)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -delete