clean:
	@find . -name '*.pyc' -delete
	
lint:
	@find delphi_core -iname "*.py" | xargs pylint
	
help:
	@echo "    clean"
	@echo "        Remove python artifacts."
	@echo "    lint"
	@echo "        Check style with pylint."