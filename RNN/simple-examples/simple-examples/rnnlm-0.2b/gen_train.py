from random import randint

write = []
valid_write = []
with open ("training_remove.txt", 'r') as files:
    print "Generating random num..."
    lines = files.readlines()
    i = 1
    while i < 100000 + 1:
        x = randint(1,5662612)
        if (len(lines[x]) > 20):
            write.append(lines[x])
            i += 1
        else:
            continue
        files.close()
with open ("training100000.txt", 'w') as files:
    print "Writing files..."
    for line in write:
        files.write(line)
    files.close()

with open ("valid100000.txt", 'w') as files:
    i = 1
    print "Writing valid files..."
    while i < 10000 + 1:
        x = randint(0,99999)
        files.write(write[x])
        i += 1
    files.close()
