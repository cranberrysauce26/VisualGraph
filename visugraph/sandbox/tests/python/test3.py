# read only should be allowed (otherwise, python won't work)
f = open("/home/steven/projects/VisualGraph/sandbox/tests/test1.py", "r")
print(f.read())