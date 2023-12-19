PYTHON = python3
MAIN_DIR = main
ARGS = $(filter-out $@,$(MAKECMDGOALS))

.PHONY: help practice1

# Set PYTHONPATH to include the project's root directory
export PYTHONPATH := $(PYTHONPATH):$(PWD)

help:
	@echo "Usage:"
	@echo "  make help - Display this help message"
	@echo "  make install - Install requirements"
	@echo "  make practice1 - Run practice1.py script"
	@echo "  make practice2 - Run practice2.py script"
	@echo "  make practice3 - Run practice3.py script"
	@echo "  make practice4 - Run practice4.py script"
	@echo "  make practice5 - Run practice5.py script"

install:
	$(PYTHON) -m pip install -r requirements.txt && \
	$(PYTHON) -c "import nltk; nltk.download('wordnet'); nltk.download('punkt')"

clean:
	rm -rf $(MAIN_DIR)/__pycache__ && \
	rm -rf manager/__pycache__ && \
	rm -rf models/__pycache__

# run practice1 script
practice1:
	$(PYTHON) $(MAIN_DIR)/practice1.py $(ARGS)

# run practice2 script
practice2:
	$(PYTHON) $(MAIN_DIR)/practice2.py $(ARGS)

# run practice3 script
practice3:
	$(PYTHON) $(MAIN_DIR)/practice3.py $(ARGS)

# run practice4 script
practice4:
	$(PYTHON) $(MAIN_DIR)/practice4.py $(ARGS)

# run practice5 script
practice5:
	$(PYTHON) $(MAIN_DIR)/practice5.py $(ARGS)

# run practice5v2 script
practice5v2:
	$(PYTHON) $(MAIN_DIR)/practice5v2.py $(ARGS)

# practice5v3 script
practice5v3:
	$(PYTHON) $(MAIN_DIR)/practice5v3.py $(ARGS)

# practice5v4 script
practice5v4:
	$(PYTHON) $(MAIN_DIR)/practice5v4.py $(ARGS)


# ------------------------------------- #
# ---------- Custom commands ---------- #
# ------------------------------------- #


baseline:
	$(PYTHON) $(MAIN_DIR)/practice5v3.py --baseline -g './/p' './/sec'  
# $(PYTHON) $(MAIN_DIR)/practice5v3.py --baseline -g './/article' && \
# $(PYTHON) $(MAIN_DIR)/practice5v3.py --baseline -g './/bdy' './/p' './/sec' './/entry' './/row' './/category' './/list' && \
# $(PYTHON) $(MAIN_DIR)/practice5v3.py --baseline -g './/p' './/sec' './/entry' './/row' './/category' './/list'

custom:
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -e --ltn -g './/p' './/sec' './/entry' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --ltc -g './/p' './/sec' './/entry' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --bm25 -g './/p' './/sec' './/entry' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -e --ltn -g './/entry' './/header'  && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --ltc -g './/entry' './/header' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --bm25 -g './/entry' './/header' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -e --ltn -g './/entry' './/category' './/row' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --ltc -g './/entry' './/category' './/row' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --bm25 -g './/entry' './/category' './/row' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -e --ltn -g './/p' './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --ltc -g './/p' './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --bm25 -g './/p' './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -e --ltn -g './/sec' './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --ltc -g './/sec' './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v3.py -i --bm25 -g './/sec' './/article'