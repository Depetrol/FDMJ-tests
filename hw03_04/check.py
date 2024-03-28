import glob
import re
import filecmp
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))



def read_file_contents(filename):
    with open(filename, 'r') as file:
        return file.read()
    

matching_files = glob.glob('./yours/*.ast') + glob.glob('./yours/*.src')

pass_all = True
print("===== Start Tests =====")
for file in matching_files:
    correct_file = os.path.join('./correct', os.path.basename(file))
    # are_same = filecmp.cmp(file, correct_file, shallow=False)
    file_contents = read_file_contents(file)
    file_contents = file_contents.replace("\r\n", "\n")
    correct_file_contents = read_file_contents(correct_file)
    correct_file_contents = correct_file_contents.replace("\r\n", "\n")
    
    diff_lines = [i for i in range(len(file_contents)) if file_contents[i] != correct_file_contents[i]]
    
    if not diff_lines: 
        print("== passed {} ==".format(file.split('/')[2]))
    else:
        print("!! failed {} !!".format(file.split('/')[2]))
        print("Different lines: ", diff_lines)
        pass_all = False
if pass_all:
    print("===== Passed All Tests =====")
else:
    print("!!!!! Some Tests Failed !!!!!")