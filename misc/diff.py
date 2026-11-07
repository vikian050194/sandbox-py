import os


def get_files(dir):
    files = []
    # r=root, d=directories, f = files
    for r, d, f in os.walk(dir):
        for file in f:
            files.append(file)
            # print(os.path.join(r, file))
    return files


# dir = os.getcwd()
sourcedir = ""
source_files = get_files(sourcedir)
source_dirs = []

targetdir = ""
target_files = get_files(targetdir)
target_dirs = []

file_in = 0
file_not_in = 0

for sfile in source_files:
    if sfile in target_files:
        file_in = file_in + 1
    else:
        file_not_in = file_not_in + 1
        print(sfile)

print(len(source_files))
print(len(target_files))
print(file_in)
print(file_not_in)
