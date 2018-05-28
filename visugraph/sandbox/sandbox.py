import subprocess
import os
import platform

sandbox_executable_path = os.path.join(os.path.dirname(__file__), 'sandbox')

class SandboxError(Exception):
    def __init__(self, return_code):
        self.return_code = return_code
        self.message = 'A sandbox error occured with return code {}'.format(self.return_code)

def execute(path_in, path_out, args, safe=True):
    if safe and platform.system() == 'Linux':
        args2 = [sandbox_executable_path, path_in, path_out]
        for a in args:
            args2.append(a)
        result = subprocess.run(args2)
        if result.returncode != 0:
            raise SandboxError(result.returncode)
    else:
        file_in = open(path_in, 'r')
        file_out = open(path_out, 'w')
        result = subprocess.run(args, stdout=subprocess.PIPE, stderr=None, input=file_in.read(), encoding='ascii')
        file_out.write(result.stdout)