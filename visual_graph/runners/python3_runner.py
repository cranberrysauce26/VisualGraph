from base_runner import BaseRunner

import subprocess

class Python3Runner(BaseRunner):

    def get_input_file_name(self):
        return 'main.py'

    def execute(self):
        args = ['python3', self.code_path]
        try:
            code_file = open(self.code_path, "r")
            output_file = open(self.output_path, "w")
            subprocess.run(args, stdin=code_file, stdout=output_file)
        except OSError as e:
            print("caught os error", e)