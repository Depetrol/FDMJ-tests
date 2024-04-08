import glob
import re
import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "yours"))
files = glob.glob("*.txt")


def read_err_line_num(filename: str) -> int:
    with open(filename, "r") as file:
        first_line: str = file.readline()
        if first_line == "":
            return -1
        return int(re.search(r"\d+", first_line).group())


pass_all: bool = True
print("===== Start Tests =====")
for file in files:
    err_line_num: int = read_err_line_num(file)
    ref_err_line_num: int = read_err_line_num(file.split(".")[0] + ".txt")

    is_same: bool = err_line_num == ref_err_line_num
    if is_same:
        print("== passed {} ==".format(file.split(".")[0]))
        print("== err_line_num:     {} ==".format(err_line_num))
        print("== ref_err_line_num: {} ==".format(ref_err_line_num))
    else:
        print("!! failed {} !!".format(file.split(".")[0]))
        pass_all = False
if pass_all:
    print("===== Passed All Tests =====")
else:
    print("!!!!! Some Tests Failed !!!!!")
