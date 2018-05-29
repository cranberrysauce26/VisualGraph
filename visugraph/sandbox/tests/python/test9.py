te = open('/usr/include/time.h', 'r').read()

i = len(te)-1
while i >= 0:
    print(te[i], end='')
    i = i-1