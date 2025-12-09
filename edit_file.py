# List of words came with different, weird formatting, this file contains scripts used to fix them

# file = open("verb_list.txt", "r")
# data = file.readlines()
# new_lines = []
# for line in data:
#     lne = line.split()
#     for word in lne:
#         word = word.lower()
#         if "\n" not in word:
#             word = word + "\n"
#         if word not in new_lines:
#             new_lines.append(word)
# file.close()

# file = open("verb_list.txt", "w")
# new_lines.sort()
# for line in new_lines:
#     file.write(line)
# file.close()

# file = open("adverb_list.txt", "r")
# data = file.readlines()
# new_lines = []
# for line in data:
#     new_lines.append(line.lower())
# file.close()
# file = open("adverb_list.txt", "w")
# new_lines.sort()
# for line in new_lines:
#     file.write(line)

# file = open("noun_list.txt", "r")
# data = file.readlines()
# new_lines = []
# for line in data:
#     lne = line.split(" ")
#     new_lines.append(lne[-1])
# file.close()
# file = open("noun_list.txt", "w")
# new_lines.sort()
# for line in new_lines:
#     file.write(line)

# file = open("noun_list.txt", "r")
# data = file.readlines()
# new_lines = []
# for line in data:
#     if line not in new_lines:
#         new_lines.append(line)
# new_lines.sort()
# file.close()
# file = open("noun_list.txt", "w")
# for line in new_lines:
#     file.write(line)

# file.close()

