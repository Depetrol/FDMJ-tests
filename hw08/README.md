# FDMJ-tests

使用方式：
- 复制Makefile
- 注释掉main.c主函数的while循环，在循环外添加以下两句：
```c
printIRP_set(IRP_parentheses);
printIRP_FuncDeclList(stderr, fdl);
```
- make test_external
- make clean_external

进行严格匹配，需要和助教给的一模一样

## makefile添加内容

FDMJ主仓库hw8的 makefile 中添加如下内容：

```makefile
TEST_EXTERNAL_DIR=../../FDMJ-tests
TEXT_EXTERNAL_HW=hw07
TESTFILE_EXTERNAL_DIR=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/test
TEST_EXTERNAL_BIN=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/bin
CHECK_PY_SCRIPT := check.py

clean_external: 
	@$(RM) $(TESTFILE_EXTERNAL_DIR)/bin
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools
	
	@find $(TESTFILE_EXTERNAL_DIR) -type f \( \
		-name "*.txt" -o -name "*.ast" -o -name "*.src" -o -name "*.xml" -o -name "*.irp" \
		-o -name "*.output" -o -name "gen_program_*" \
	\) -exec $(RM) {} \; ;\
	
SHELL:=/bin/bash

test_external: clean build clean_external
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@cp $(MAIN_EXE) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools/main
	@cp $(AST2IRP) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools/std
	@cd $(TESTFILE_EXTERNAL_DIR);pwd; \
	$(RANDOM_CODE_GEN) \
	for file in $$(ls .); do \
		if [ "$${file##*.}" = "fmj" ]; then \
			$(FMJ2AST) "$${file%%.*}"; \
			$(MAIN_EXE) "$${file%%.*}" &> "../yours/$${file%%.*}".txt; \
			$(AST2IRP) "$${file%%.*}"; \
			mv "$${file%%.*}.3.irp" "../correct/$${file%%.*}".txt; \
		fi; \
	done; \
	python3 ../${CHECK_PY_SCRIPT}; \
	cd $(CURDIR)
```