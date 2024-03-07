import glob
import re
import filecmp
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
files = glob.glob('*')

pattern = re.compile(r'.*\.output$')

def read_file_contents(filename):
    with open(filename, 'r') as file:
        return file.read()

matching_files = [file for file in files if pattern.match(file)]
matching_files.sort()
pass_all = True
print("===== Start Tests =====")
for file in matching_files:
    correct_file = file.split('.')[0] + '.correct'
    # are_same = filecmp.cmp(file, correct_file, shallow=False)
    file_contents = read_file_contents(file)
    correct_file_contents = read_file_contents(correct_file)
    are_same = file_contents == correct_file_contents
    if are_same: 
        print("== passed {} ==".format(file.split('.')[0]))
    else:
        print("!! failed {} !!".format(file.split('.')[0]))
        pass_all = False
if pass_all:
    print("===== Passed All Tests =====")
else:
    print("!!!!! Some Tests Failed !!!!!")