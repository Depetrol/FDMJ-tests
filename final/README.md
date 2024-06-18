```makefile
TEST_EXTERNAL_DIR=../../FDMJ-tests
TEXT_EXTERNAL_HW=final
TESTFILE_EXTERNAL_DIR=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/test
TEST_EXTERNAL_BIN=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/bin
CHECK_PY_SCRIPT := check.py

clean_external: 
	@$(RM) $(TESTFILE_EXTERNAL_DIR)/bin
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools
	
	@find $(TESTFILE_EXTERNAL_DIR) -type f \( \
		-name "*.txt" -o -name "*.ast" -o -name "*.src" -o -name "*.xml" -o -name "*.irp" -o -name "*.stm" -o -name "*.s" \
		-o -name "*.output" -o -name "gen_program_*" -o -name "*.ins" -o -name "*.cfg" -o -name "*.ssa" -o -name "*.arm" \
		-o -name "*.ll" \
	\) -exec $(RM) {} \; ;\
	
SHELL:=/bin/bash

test_external: clean build clean_external
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@cd $(TESTFILE_EXTERNAL_DIR);pwd; \
	for file in $$(ls .); do \
		if [ "$${file##*.}" = "fmj" ]; then \
			cp "$${file%%.*}.ans" "../correct/$${file%%.*}".txt; \
			$(MAIN_EXE) "$${file%%.*}" < "$${file%%.*}".fmj; \
			$(LLVMLINK) --opaque-pointers "$${file%%.*}".6.ssa $(BUILD_DIR)/vendor/libsysy/libsysy64.ll -S -o "$${file%%.*}".ll && \
			$(LLI) -opaque-pointers "$${file%%.*}".ll > "$${file%%.*}".llvm.output && \
			mv "$${file%%.*}.llvm.output" "../yours/$${file%%.*}".llvm.txt; \
			$(ARMCC) -mcpu=cortex-a72 "$${file%%.*}".8.s $(BUILD_DIR)/vendor/libsysy/libsysy32.s --static -o "$${file%%.*}".s && \
			$(QEMU) -B 0x1000 "$${file%%.*}".s > "$${file%%.*}".rpi.output && \
			mv "$${file%%.*}.rpi.output" "../yours/$${file%%.*}".rpi.txt; \
		fi; \
	done; \
	python3 ../${CHECK_PY_SCRIPT}; \
	cd $(CURDIR)
```