#### DEFINITIONS ####

PYTHON := $(shell command -v python3 2>/dev/null || command -v python 2>/dev/null)

all: run

run:
	$(PYTHON) code/geography.py