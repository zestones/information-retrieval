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


# run practice5 script with custom parameters 
custom_practice5:
	$(PYTHON) $(MAIN_DIR)/practice5.py -e --ltn --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt && \
	$(PYTHON) $(MAIN_DIR)/practice5.py -i --ltc --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt && \
	$(PYTHON) $(MAIN_DIR)/practice5.py -i --bm25 --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt

# run practice5v2 script with custom parameters
custom:
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -e --ltn --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --ltc --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --bm25 --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/article' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -e --ltn --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/p' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --ltc --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/p' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --bm25 --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/p' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -e --ltn --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/sec' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --ltc --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/sec' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --bm25 --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/sec' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -e --ltn --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/header' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --ltc --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/header' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --bm25 --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/header' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -e --ltn --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/bdy' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --ltc --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/bdy' && \
	$(PYTHON) $(MAIN_DIR)/practice5v2.py -i --bm25 --query-file ../lib/data/practice_04/topics_M2DSC_7Q.txt -g './/bdy'