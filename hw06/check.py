import glob
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_file_contents(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

matching_files = glob.glob('./yours/*.txt')

pass_all = True
passed_prints = []
failed_prints = []
print("===== Start Tests =====")
for file in matching_files:
    correct_file = os.path.join('./correct', os.path.basename(file))
    file_contents = read_file_contents(file)
    correct_file_contents = read_file_contents(correct_file)
    
    min_len = min(len(file_contents), len(correct_file_contents))
    diff_lines = [i + 1 for i in range(min_len) if file_contents[i] != correct_file_contents[i]]
    
    failed_msg = ""
    if not diff_lines: 
        if len(file_contents) != len(correct_file_contents):
            failed_msg = "!! failed {} !!".format(file.split('/')[2]) + "\n\t" + "Different number of lines, though existing lines are the same."
            pass_all = False
        else:
            passed_prints.append("== passed {} ==".format(file.split('/')[2]))
    else:
        failed_msg = "!! failed {} !!".format(file.split('/')[2]) + "\n\t" + "different line: " + str(diff_lines)
        pass_all = False
    if failed_msg != "":
        failed_prints.append(failed_msg)

if pass_all:
    for passed_print in passed_prints:
        print(passed_print)
    print("===== Passed All Tests =====")
else:
    # 将 failed_prints按照名称排序后打印
    failed_prints.sort()
    for failed_print in failed_prints:
        print(failed_print)
    print("!!!!! Some Tests Failed !!!!!")
