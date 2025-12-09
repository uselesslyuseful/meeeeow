import random

MEOW_LIST = {"pronoun":"mrrp", "noun":"mrrau", "verb":"nya", "adjective":"mrowl", "adverb":"hrru"}
with open("noun_list.txt", "r") as file:
    NOUNS = file.readlines()
with open("verb_list.txt", "r") as file:
    VERBS = file.readlines()
with open("adverb_list.txt", "r") as file:
    ADVERBS = file.readlines()
with open("adjective_list.txt", "r") as file:
    ADJECTIVES = file.readlines()
with open("pronoun_list.txt", "r") as file:
    PRONOUNS = file.readlines()

for i in range(len(NOUNS)):
    NOUNS[i] = NOUNS[i][:-1]
for i in range(len(PRONOUNS)):
    PRONOUNS[i] = PRONOUNS[i][:-1]
for i in range(len(ADVERBS)):
    ADVERBS[i] = ADVERBS[i][:-1]
for i in range(len(VERBS)):
    VERBS[i] = VERBS[i][:-1]
for i in range(len(ADJECTIVES)):
    ADJECTIVES[i] = ADJECTIVES[i][:-1]

def convert_to_meow(inp:str):
    inp_list = inp.split()
    converted = []
    for word in inp_list:
        state = "lowercase"
        if word.isupper():
            state = "all_upper"
        elif word[0].isupper():
            state = "capital"
        word = word.lower()

        if word in PRONOUNS:
            base_word = MEOW_LIST["pronoun"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:2] + ((len(word)-5)//2) * "r" + base_word[2:]
            else:
                new_word = base_word
        elif word in VERBS:
            base_word = MEOW_LIST["verb"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word + ((len(word)-5)//2) * "~a"
            else:
                new_word = base_word
        elif word in ADVERBS:
            base_word = MEOW_LIST["adverb"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:2] + ((len(word)-5)//2) * "r" + base_word[2:]
            else:
                new_word = base_word
        elif word in ADJECTIVES:
            base_word = MEOW_LIST["adjective"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:2] + ((len(word)-5)//2) * "o" + base_word[2:]
            else:
                new_word = base_word
        elif word in NOUNS:
            base_word = MEOW_LIST["noun"]
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:3] + ((len(word)-5)//2) * "a" + base_word[3:]
            else:
                new_word = base_word
        else:
            base_word = "meow"
            new_word = base_word
            if len(word) >= 5:
                new_word = base_word[:1] + ((len(word)-5)//2) * "e" + base_word[1:]
            else:
                new_word = base_word
        if state == "all_upper":
            converted.append(new_word.upper())
        elif state == "capital":
            converted.append(new_word[0].upper() + new_word[1:])
        else:
            converted.append(new_word)
    return " ".join(converted)

inp = input("Enter the message you want to convert: ")
print(convert_to_meow(inp))