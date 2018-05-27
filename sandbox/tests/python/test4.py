# read only should be allowed (otherwise, python won't work)
# but write is not allowed
f = open("/home/steven/projects/VisualGraph/sandbox/tests/test1.py", "w")
print(f.read())