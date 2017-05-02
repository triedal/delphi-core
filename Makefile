clean:
	@find . -name '*.pyc' -delete
	
lint:
	@find delphi_core -iname "*.py" | xargs pylint
	
test:
	@pytest
	
help:
	@echo "    clean"
	@echo "        Remove python artifacts."
	@echo "    lint"
	@echo "        Check style with pylint."
	@echo "	   test"
	@echo "		   Runs unit tests."