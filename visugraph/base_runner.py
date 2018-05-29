import uuid
import os
import shutil
import json
from visugraph.sandbox import SandboxError

# TODO: errors
class BaseRunner:

    '''
    The BaseRunner class manages creating temporary folders, copying user code to a file in that folder, and creating an output file to read the trace as json.
    self.code is the user's code as a string.
    self.root_folder is the user's temporary folder. It is creating by adding a random uuid to the tmp_folder parameter passed into the constructor.
    self.input_path is the path to the user's code file.
    self.output_path is the path to the trace json file.
    The only interface method is self.run, which returns the json string and performs cleanup
    '''

    # TODO: maybe a symlink would be more efficient?
    def __init__(self, code_str, tmp_folder, code_fname='code.in', output_fname='trace.json', copy_dir=None, cleanup=True):
        '''
        code_str is the user's code
        tmp_folder is the absolute path to temporary folder root where I should create my sub folder
        code_fname is the name of the user's code file, which defaults to code.in
        output_fname is the name of the file to output to, which defaults to trace.json
        copy_dir is the absolute path to the folder that we want to copy into the user's temporary folder.
        If copy_dir == None, no copying is done
        '''
        self.code = code_str
        self.root_folder = os.path.join(tmp_folder, str(uuid.uuid4()))
        while os.path.exists(self.root_folder):
            print('This should not be called')
            self.root_folder = os.path.join(tmp_folder, str(uuid.uuid4()))

        if copy_dir != None:
            shutil.copytree(copy_dir, self.root_folder)
        else:
            os.makedirs(self.root_folder)

        self.input_path = os.path.join(self.root_folder, code_fname)
        self.output_path = os.path.join(self.root_folder, output_fname)

        with open(self.output_path, 'w'), open(self.input_path, 'w') as code_file:
            code_file.write(self.code)
        
        self.should_cleanup = cleanup

    # to be overwridden by the base class
    # TODO: Is the callback necessary? I think python is blocking by default.
    def _execute(self):
        raise NotImplementedError()

    # main function
    def run(self):
        self._setup_env()
        try:
            self._execute()
        except SandboxError as e:
            tr = {'error': e.message}
            return json.dumps(tr)
        except Exception as e:
            tr = {'error': 'An unknown error occured: {}'.format(str(e))}
            return json.dumps(tr)
        json_str = self._read_result()
        self._cleanup()
        return json_str

    # additional setup
    def _setup_env(self):
        pass
    
    def _cleanup(self):
        if not self.should_cleanup:
            return
        # comment out code below to see the actual tmp folder
        if not os.path.exists(self.root_folder):
            return
        try:
            shutil.rmtree(self.root_folder)
        except OSError as e:
            print('could not remove root folder. error is', e)

    def __del__(self):
        self._cleanup()
    
    def _read_result(self):
        with open(self.output_path, 'r') as f:
            return f.read()