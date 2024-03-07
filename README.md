# FDMJ-tests

## 运行Test

* 将需要的 `.fdmj`和.`correct`文件复制到对应的 `/test`文件夹下
* 将 `check.py`复制到 `/test`文件夹下
* 将 `random.py`复制到 `/test`文件夹下
* 运行 `make test`生成 `.output`
* 运行 `python check.py`比较 `.fdmj`和 `.correct`文件
* 
* 


## 贡献测试样例

* 先fork本仓库
* 做出修改（提交新的 `.output` 和 `.correct`）文件
* 然后提出PR到Main分支
