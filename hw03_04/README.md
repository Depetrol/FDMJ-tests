### 使用方式：

保持源代码仓库和测试仓库在同一级

在源代码仓库2024/hw3_4/Makefile中添加

```makefile
EXTERNAL_TEST_DIR = $(abspath $(CURDIR)/../../FDMJ-tests/hw03_04)
EXTERAL_FMJ2ST = $(EXTERNAL_TEST_DIR)/tools/fmj2ast
clean-external:
	@find $(EXTERNAL_TEST_DIR)/yours -type f \( \
		-name "*.src" -o -name "*.ast" -o -name "*.output" \
		\) -exec $(RM) {} \;
	@find $(EXTERNAL_TEST_DIR)/correct -type f \( \
		-name "*.src" -o -name "*.ast" -o -name "*.output" \
		\) -exec $(RM) {} \;
	@find $(EXTERNAL_TEST_DIR)/test -type f \( \
		-name "*.src" -o -name "*.ast" -o -name "*.output" \
		\) -exec $(RM) {} \;

test-external: clean-external
	@cd $(EXTERNAL_TEST_DIR)/test && \
	for file in *; do \
		if [ "$${file##*.}" = "fmj" ]; then \
			echo "[$${file%%.*}]"; \
			$(MAIN_EXE) "$${file%%.*}" < "$${file}" > ../yours/"$${file%%.*}".output; \
		fi \
	done; \
	find $(EXTERNAL_TEST_DIR)/test -type f \( \
		-name "*.src" -o -name "*.ast" -o -name "*.output" \
		\) -exec mv {} $(EXTERNAL_TEST_DIR)/yours/ \; && \
	for file in *; do \
		if [ "$${file##*.}" = "fmj" ]; then \
			echo "[$${file%%.*}]"; \
			$(EXTERAL_FMJ2ST) "$${file%%.*}" < "$${file}" > ../correct/"$${file%%.*}".output; \
		fi \
	done; \
	find $(EXTERNAL_TEST_DIR)/test -type f \( \
		-name "*.ast" -o -name "*.src" -o -name "*.output" \
		\) -exec mv {} $(EXTERNAL_TEST_DIR)/correct/ \;
	cd $(EXTERNAL_TEST_DIR); \
	python3 check.py; \
	cd $(CURDIR)

```

运行

```shell
$ make test-external
```



### 贡献测试用例方式：

在该仓库./hw03_04/test中加入.fmj文件即可