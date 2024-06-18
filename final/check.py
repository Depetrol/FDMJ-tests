import glob
import os

RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
RESET = '\033[0m'

# 确保工作目录是脚本所在目录
os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_file_contents(filename):
    """读取文件内容，返回一个由行组成的列表"""
    if not os.path.exists(filename):
        return []
    with open(filename, 'r') as file:
        return file.read().splitlines()

# 匹配所有的测试结果文件
correct_matching_files = glob.glob('./correct/*.txt')

# 初始化测试通过与否的标志
pass_all = True
passed_prints = []
failed_prints = []
print("===== Start Tests =====")
for correct_file in correct_matching_files:
    llvm_passed, rpi_passed = True, True
    llvm_file = correct_file.replace("correct", "yours").replace(".txt", ".llvm.txt")
    rpi_file = correct_file.replace("correct", "yours").replace(".txt", ".rpi.txt")
    
    print(f"{os.path.basename(correct_file)}: ".ljust(15), end="")
    
    correct_file_contents = read_file_contents(correct_file)
    llvm_file_contents = read_file_contents(llvm_file)
    rpi_file_contents = read_file_contents(rpi_file)
    
    # compare llvm
    min_len = min(len(llvm_file_contents), len(correct_file_contents))
    
    diff_lines = [(i + 1, correct_file_contents[i], llvm_file_contents[i]) 
                  for i in range(min_len) if llvm_file_contents[i] != correct_file_contents[i]]
    
    llvm_failed_msg = f"{YELLOW}llvm{RESET}: \n"
    if len(llvm_file_contents) != len(correct_file_contents):
        llvm_passed = False
        llvm_failed_msg += f"expect {len(correct_file_contents)} lines. but got {len(llvm_file_contents)} lines.\n"
    
    if diff_lines: 
        llvm_passed = False
        for diff_line in diff_lines:
            llvm_failed_msg += f"different at line {diff_line[0]}:\n"
            llvm_failed_msg += f"\texpect: {diff_line[1]}\n"
            llvm_failed_msg += f"\tgot: {diff_line[2]}\n"
    
    # compare rpi
    min_len = min(len(rpi_file_contents), len(correct_file_contents))
    
    diff_lines = [(i + 1, correct_file_contents[i], rpi_file_contents[i]) 
                  for i in range(min_len) if rpi_file_contents[i] != correct_file_contents[i]]
    
    rpi_failed_msg = f"{YELLOW}rpi{RESET}: \n"
    if len(rpi_file_contents) != len(correct_file_contents):
        rpi_passed = False
        rpi_failed_msg += f"expect {len(correct_file_contents)} lines. but got {len(rpi_file_contents)} lines.\n"
    
    if diff_lines: 
        rpi_passed = False
        for diff_line in diff_lines:
            rpi_failed_msg += f"different at line {diff_line[0]}:\n"
            rpi_failed_msg += f"\texpect: {diff_line[1]}\n"
            rpi_failed_msg += f"\tgot: {diff_line[2]}\n"

    if llvm_passed:
        print(f"llvm {GREEN}passed{RESET}, ", end="")
    else:
        print(f"llvm {RED}failed{RESET}, ", end="")
        
    if rpi_passed:
        print(f"rpi {GREEN}passed{RESET}")
    else:
        print(f"rpi {RED}failed{RESET}")
        
    if not llvm_passed:
        print(llvm_failed_msg)
    
    if not rpi_passed:
        print(rpi_failed_msg)
        

