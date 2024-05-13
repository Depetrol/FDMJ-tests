import glob
import os

# 确保工作目录是脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_file_contents(filename):
    """读取文件内容，返回一个由行组成的列表"""
    with open(filename, 'r') as file:
        return file.read().splitlines()

# 匹配所有的测试结果文件
matching_files = glob.glob('./yours/*.txt')

# 初始化测试通过与否的标志
pass_all = True
passed_prints = []
failed_prints = []
print("===== Start Tests =====")
for file in matching_files:
    correct_file = os.path.join('./correct', os.path.basename(file))
    file_contents = read_file_contents(file)
    correct_file_contents = read_file_contents(correct_file)
    
    # 获取两个文件内容的最小长度
    min_len = min(len(file_contents), len(correct_file_contents))
    # 收集所有不同的行号和内容
    diff_lines = [(i + 1, file_contents[i], correct_file_contents[i]) 
                  for i in range(min_len) if file_contents[i] != correct_file_contents[i]]
    
    failed_msg = ""
    if not diff_lines: 
        if len(file_contents) != len(correct_file_contents):
            failed_msg = "!! failed {} !!".format(file.split('/')[2]) + "\n\t" + "Different number of lines, though existing lines are the same."
            pass_all = False
        else:
            passed_prints.append("== passed {} ==".format(file.split('/')[2]))
    else:
        failed_msg = "!! failed {} !!".format(file.split('/')[2]) + "\n\t" + \
                     "different line(s): " + ", ".join([str(ln) for ln, _, _ in diff_lines]) + "\n" + \
                     "\n".join([f"\tLine {ln}: \n\tYou: '{y}' \n\tRef: '{c}'" for ln, y, c in diff_lines])
        pass_all = False
    if failed_msg != "":
        failed_prints.append(failed_msg)

if pass_all:
    passed_prints.sort()
    for passed_print in passed_prints:
        print(passed_print)
    print("===== Passed All Tests =====")
else:
    failed_prints.sort()
    for failed_print in failed_prints:
        print(failed_print)
    print("!!!!! Some Tests Failed !!!!!")
