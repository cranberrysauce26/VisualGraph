import uuid
import os
import shutil

class BaseRunner:

    # to be overwridden by the base class
    def execute(self):
        raise NotImplementedError()

    # to be overwridde by the base class
    def get_input_file_name(self):
        return 'main.in'

    def __init__(self, code_str, tmp_folder):
        self.code = code_str
        self.root_folder = os.path.join(tmp_folder, str(uuid.uuid4()))
        self.output_path = os.path.join(self.root_folder, 'trace.json')
        self.code_path = os.path.join(self.root_folder, self.get_input_file_name())
        while os.path.exists(self.root_folder):
            print("This should not be called")
            self.root_folder = os.path.join(tmp_folder, str(uuid.uuid4()))

    # main function
    def run(self):
        self.setup_env()
        self.execute()
        json_str = self.read_result()
        self.cleanup()
        return json_str

    def setup_env(self):
        try:
            print("in setup env")
            os.makedirs(self.root_folder)
            with open(self.output_path, 'w'):
                pass
            with open(self.code_path, 'w') as output_file:
                output_file.write(self.code)
        except OSError as e:
            print("Could not setup environment. error is", e)
    
    def cleanup(self):
        # comment out code below to see the actual tmp folder
        try:
            shutil.rmtree(self.root_folder)
        except OSError as e:
            print("could not remove root folder. error is", e)

    def __del__(self):
        self.cleanup()
    
    def read_result(self):
        with open(self.output_path, "r") as f:
            return f.read()
