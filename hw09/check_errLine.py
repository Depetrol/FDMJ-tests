import glob
import re
import os

os.chdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), "yours"))
files = glob.glob("*.txt")
files.sort()


def read_err_line_num(filename: str) -> int:
    with open(filename, "r") as file:
        first_line: str = file.readline()
        if first_line == "":
            return -1
        return int(re.search(r"\d+", first_line).group())


pass_all: bool = True
failed_files: list = []
print("===== Start Tests =====")
for file in files:
    err_line_num: int = read_err_line_num(file)
    ref_err_line_num: int = read_err_line_num("../correct/" + file)

    is_same: bool = err_line_num == ref_err_line_num
    print("== err_line_num:     {} ==".format(err_line_num))
    print("== ref_err_line_num: {} ==".format(ref_err_line_num))
    if is_same:
        print("== passed {} ==".format(file.split(".")[0]))
    else:
        print("!! failed {} !!".format(file.split(".")[0]))
        pass_all = False
        failed_files.append(file)
if pass_all:
    print("\n===== Passed All Tests =====")
else:
    print("\n!!!!! Some Tests Failed !!!!!")
    print("Failed files:")
    for file in failed_files:
        print("\t", file)
