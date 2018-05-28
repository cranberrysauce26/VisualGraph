import subprocess
import os

sandbox_executable_path = os.path.join(os.path.dirname(__file__), 'sandbox')

def execute(path_in, path_out, args):
    args2 = [sandbox_executable_path, path_in, path_out]
    for a in args:
        args2.append(a)
    subprocess.run(args2)