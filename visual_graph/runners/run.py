# import visual_graph.exceptions
from python2_runner import Python2Runner
from python3_runner import Python3Runner

def run_and_return_trace(code_str, lang, tmp_folder):
    runner = None
    if lang=='python2':
        runner = Python2Runner(code_str, tmp_folder)
    elif lang=='python3':
        runner = Python3Runner(code_str, tmp_folder)
    else:
        pass
        # raise visual_graph.exceptions.LanguageNotFoundError()

    # if runner is None, you have an error!
    returned_json = runner.run()
    return returned_json

if __name__ == '__main__':
    import os
    tmpfolder = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../../tmp')

    code_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), '../example_code/example1.py')
    code = open(code_file, 'r').read()
    print("code is:", code)
    returned_json = run_and_return_trace(code, 'python2', tmpfolder)
    print("returned_json:", returned_json)