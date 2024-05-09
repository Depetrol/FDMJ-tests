```makefile
TEST_EXTERNAL_DIR=../../FDMJ-tests
TEXT_EXTERNAL_HW=hw09
TESTFILE_EXTERNAL_DIR=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/test
TEST_EXTERNAL_BIN=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/bin
CHECK_PY_SCRIPT := check.py

clean_external: 
	@$(RM) $(TESTFILE_EXTERNAL_DIR)/bin
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools
	
	@find $(TESTFILE_EXTERNAL_DIR) -type f \( \
		-name "*.txt" -o -name "*.ast" -o -name "*.src" -o -name "*.xml" -o -name "*.irp" -o -name "*.stm"\
		-o -name "*.output" -o -name "gen_program_*" \
	\) -exec $(RM) {} \; ;\
	
SHELL:=/bin/bash

test_external: clean build clean_external
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@cp $(MAIN_EXE) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools/main
	@cp $(IRP2LLVM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools/std
	@cd $(TESTFILE_EXTERNAL_DIR);pwd; \
	for file in $$(ls .); do \
		if [ "$${file##*.}" = "fmj" ]; then \
			$(FMJ2AST) "$${file%%.*}"; \
			$(AST2IRP) -f xml "$${file%%.*}"; \
			$(MAIN_EXE) "$${file%%.*}"; \
			mv "$${file%%.*}.5.ins" "../yours/$${file%%.*}".txt; \
			$(IRP2LLVM) "$${file%%.*}"; \
			mv "$${file%%.*}.5.ins" "../correct/$${file%%.*}".txt; \
		fi; \
	done; \
	python3 ../${CHECK_PY_SCRIPT}; \
	cd $(CURDIR)
```