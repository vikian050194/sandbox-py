output = "output.txt"
min = 0
max = 10

lines = []

for x in range(min, max + 1):
    lines.append(f"{x}\n")

with open(output, 'w') as out_file:
    out_file.writelines(lines)


# outF = open("myOutFile.txt", "w")
# for line in textList:
#   # write line to output file
#   outF.write(line)
#   outF.write("\n")
# outF.close()


# outF = open("myOutFile.txt", "w")
# for line in textList:
#   print >>outF, line
# outF.close()


# outF = open(output, "w")
# outF.writelines(lines)
# outF.close()