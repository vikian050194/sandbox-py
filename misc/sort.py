lines = []

file = "output.txt"

with open(file, "r") as default_branch:
    lines = default_branch.readlines()
repos = set(lines)
sort_file = file[:-4] + "_sorted" + file[-4:]
with open(sort_file, "w") as default_branch:
    default_branch.writelines(sorted(repos))
