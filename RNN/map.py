import re

def make_dict(name):
    my_dict = dict()
    with open (name, 'r') as inputfile:
        print "Making dict..."
        lines = inputfile.readlines()
        for line in lines:
            (key, value) = tuple(re.split(r'\t+',line))
            my_dict[key] = value
        print my_dict
        inputfile.close()
    return my_dict

def main():
    make_dict("timit.chmap")

if __name__ == "__main__":
    main()
