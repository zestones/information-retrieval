PYTHON = python3
PRACTICE_DIR = practice
ARGS = $(filter-out $@,$(MAKECMDGOALS))

.PHONY: help practice1

# Set PYTHONPATH to include the project's root directory
export PYTHONPATH := $(PYTHONPATH):$(PWD)

help:
	@echo "Usage:"
	@echo "  make help - Display this help message"
	@echo "  make practice1 - Run practice1.py script"

# run practice1 script
practice1:
	$(PYTHON) $(PRACTICE_DIR)/practice1.py $(ARGS)

# run practice2 script
practice2:
	$(PYTHON) $(PRACTICE_DIR)/practice2.py $(ARGS)