import re

def make_dict():
    my_dict = dict()
    print "Making dict..."
    with open ("timit.chmap", 'r') as inputfile:
        lines = inputfile.readlines()
        for line in lines:
            (key, value) = tuple(re.split(r'\t+',line))
            my_dict[key] = value
        inputfile.close()
    return my_dict

def use_dict(in_dict, in_line):
    word_list = re.split(r' +', in_line)
    strs = ""
    for word in word_list[:-1]:
        strs += in_dict[word][:-1]
    return strs
