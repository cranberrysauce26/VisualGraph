import os
import json
import subprocess

from visugraph.base_runner import BaseRunner
import visugraph.sandbox as sandbox


class Python3Runner(BaseRunner):

    def _execute(self):
        '''
        This function tells sandbox to execute the command: /usr/bin/python3 -B {tracer_path}
        where tracer_path is the path to the tracer.py file in the user's temporary folder.
        The -B flag is to prevent writing to __pycache__.
        TODO: make sandbox intelligently determine what write calls to kill to eliminate -B
        '''
        py3_folder = os.path.abspath(os.path.dirname(__file__))
        tracer_path = os.path.join(py3_folder, 'user/tracer.py')
        sandbox.execute(self.input_path, self.output_path, [
                        '/usr/bin/python3', '-B', tracer_path], safe=False)


def get_trace(code):
    '''
    code is the user's code as a string
    it returns the trace as json
    '''
    py3_folder = os.path.abspath(os.path.dirname(__file__))
    tmp_folder = os.path.join(py3_folder, 'tmp')
    # user_folder = os.path.join(py3_folder, 'user')
    runner = Python3Runner(
        code, tmp_folder, code_fname='main.py', copy_dir=None, cleanup=True)
    return runner.run()


if __name__ == '__main__':
    '''
    This prints the json trace from every example in visugraph/py3/example_code
    To run it, go to the project root folder and enter the command
    python -m visugraph.py3.runner
    '''
    code_example_folder = os.path.join(os.path.abspath(
        os.path.dirname(__file__)), 'example_code')

    i = 1
    code_path = os.path.join(code_example_folder, 'example{}.py'.format(i))
    while os.path.exists(code_path):
        with open(code_path, 'r') as code_file:
            code_str = code_file.read()
            print(code_path)
            print(get_trace(code_str))
            print()
        i += 1
        code_path = os.path.join(code_example_folder, 'example{}.py'.format(i))
