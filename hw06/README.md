# FDMJ-tests

使用方式：
- FDMJ主仓库hw6的 makefile 中添加新的命令-->[makefile命令](#makefile添加内容)
- 可能需要手动修改FDMJ主仓库中tool目录下可执行文件的权限
	- `tools/ast2irp`
	- `tools/astcheck`
	- `tools/fmj2ast`
- 运行 `make test_external`命令来重新构建最新的源代码，复制main文件到本仓库的bin/hwx/main，并运行对应的test
- 运行 `make clean_external`命令清除在测试仓库生成的文件
- 新增一些参数，方便测试
	- 通过 `RANDOM=1` 启用随机测试（class相关的随机测试未更新）
		- `RANDOM=0` 默认不启用
	- 通过 `CHECK` 指定检查脚本
		- `check.py` 会对输出进行严格检查
		- `check_errLine.py` 只会检查行号
		- 默认`check.py`
	- 通过 `INFO` 指定是否输出当前运行的程序信息
		- `INFO=0` 不输出
		- `INFO=1` 输出
	- 通过 `CLEAN_RANDOM=1` 删除随机测试的`.fmj`文件

```shell
# 默认 RANDOM=0 CHECK=check.py INFO=0
make test_external
make test_external RANDOM=1 CHECK=check_errLine.py INFO=0
make test_external RANDOM=0 CHECK=check_errLine.py INFO=0
make test_external RANDOM=1 CHECK=check.py INFO=0
make test_external RANDOM=0 CHECK=check.py INFO=0
# 默认 CLEAN_RANDOM=0
make clean_external
make clean_external CLEAN_RANDOM=1
make clean_external CLEAN_RANDOM=0
```

## makefile添加内容

FDMJ主仓库hw6的 makefile 中添加如下内容：

```makefile
TEST_EXTERNAL_DIR=../../FDMJ-tests
TEXT_EXTERNAL_HW=hw06
TESTFILE_EXTERNAL_DIR=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/test
TEST_EXTERNAL_BIN=$(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/bin

RUN_RANDOM_CODE_GEN := 0
CHECK_PY_SCRIPT := check.py
PRINT_INFO := 0
CLEAN_RANDOM_TEST := 0

# 如果在命令行中传递了 RANDOM=1，则启动随机代码生成
ifdef RANDOM
	RUN_RANDOM_CODE_GEN := $(RANDOM)
endif

ifeq ($(RUN_RANDOM_CODE_GEN), 1)
    RANDOM_CODE_GEN := python3 randomCodeGen_v2.py;
endif

# 如果在命令行中传递了 CHECK，则设置使用的检查脚本
ifdef CHECK
    CHECK_PY_SCRIPT := $(CHECK)
endif

# 如果在命令行中传递了 INFO，则设置是否打印额外信息
ifdef INFO
	PRINT_INFO := $(INFO)
endif

ifdef CLEAN_RANDOM
	CLEAN_RANDOM_TEST := $(CLEAN_RANDOM)
endif

clean_external: 
	@$(RM) $(TESTFILE_EXTERNAL_DIR)/bin
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@$(RM) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools
	
	@if [ "$(CLEAN_RANDOM_TEST)" = "1" ]; then \
		find $(TESTFILE_EXTERNAL_DIR) -type f \( \
			-name "*.txt" -o -name "*.ast" -o -name "*.src" -o -name "*.xml" \
			-o -name "*.output" -o -name "gen_program_*" -o -name "myRandomTest*.fmj" \
		\) -exec $(RM) {} \; ;\
	else \
		find $(TESTFILE_EXTERNAL_DIR) -type f \( \
			-name "*.txt" -o -name "*.ast" -o -name "*.src" -o -name "*.xml" \
			-o -name "*.output" -o -name "gen_program_*" \
		\) -exec $(RM) {} \; ;\
	fi
	
SHELL:=/bin/bash

test_external: clean build clean_external
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/yours
	@mkdir -p $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/correct
	@cp $(MAIN_EXE) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools/main
	@cp $(ASTCHECK) $(TEST_EXTERNAL_DIR)/$(TEXT_EXTERNAL_HW)/tools/std
	@cd $(TESTFILE_EXTERNAL_DIR);pwd; \
	$(RANDOM_CODE_GEN) \
	for file in $$(ls .); do \
		if [ "$${file##*.}" = "fmj" ]; then \
			if [ $(PRINT_INFO) -eq 1 ]; then \
				echo "[$${file%%.*}]"; \
				echo "running fmj to ast code..."; \
			fi; \
			$(FMJ2AST) "$${file%%.*}"; \
			if [ $(PRINT_INFO) -eq 1 ]; then \
				echo "running your code..."; \
			fi; \
			$(MAIN_EXE) "$${file%%.*}" &> "../yours/$${file%%.*}".txt; \
			if [ $(PRINT_INFO) -eq 1 ]; then \
				echo "running standard code..."; \
			fi; \
			$(ASTCHECK) "$${file%%.*}" &> "../correct/$${file%%.*}".txt; \
		fi; \
	done; \
	python3 ../${CHECK_PY_SCRIPT}; \
	cd $(CURDIR)
```