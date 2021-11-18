import sys

for line in sys.stdin:
    line = line.strip()
    temperature = int(line[87:92])
    quality = int(line[92])
    accepted_quality = [0,1,4,5,9]
    if ((temperature != 9999) and quality in accepted_quality):
        print('%s\t%d' % (line[15:23], int(line[87:92])))