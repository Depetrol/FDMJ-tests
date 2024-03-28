import glob
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))

def read_file_contents(filename):
    with open(filename, 'r') as file:
        return file.read().splitlines()

matching_files = glob.glob('./yours/*.ast') + glob.glob('./yours/*.src')

pass_all = True
print("===== Start Tests =====")
for file in matching_files:
    correct_file = os.path.join('./correct', os.path.basename(file))
    file_contents = read_file_contents(file)
    correct_file_contents = read_file_contents(correct_file)
    
    min_len = min(len(file_contents), len(correct_file_contents))
    diff_lines = [i + 1 for i in range(min_len) if file_contents[i] != correct_file_contents[i]]
    
    if not diff_lines: 
        if len(file_contents) != len(correct_file_contents):
            print("!! failed {} !!".format(file.split('/')[2]))
            print("Different number of lines, though existing lines are the same.")
            pass_all = False
        else:
            print("== passed {} ==".format(file.split('/')[2]))
    else:
        print("!! failed {} !!".format(file.split('/')[2]))
        print("different line: ", diff_lines)
        pass_all = False

if pass_all:
    print("===== Passed All Tests =====")
else:
    print("!!!!! Some Tests Failed !!!!!")
