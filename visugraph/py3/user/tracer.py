import bdb
import json
import sys  # for getting main arguments
import pybox
from trace_entry import TraceEntry, TraceEntryJSONEncoder

MAX_USER_LINES = 300
MAX_FUNCTION_CALLS = 300
MAX_TOTAL_LINES = 10000


class Tracer(bdb.Bdb):

    def __init__(self):
        bdb.Bdb.__init__(self)
        self.trace = []
        self.last_line = -1
        self.number_of_user_lines = 0
        self.number_of_total_lines = 0
        self.numer_of_function_calls = 0

    # main function
    # it executes the code and returns the trace
    def execute(self, code_str, builtins=__builtins__):
        self.trace = []
        # This causes errors for me!?!
        safe_globals = pybox.safe_globals(builtins)
        try:
            self.run(code_str, safe_globals, safe_globals)
            # self.run(code_str)
        except Exception as e:
            self.trace.append(TraceEntry(error=str(e)))

    def user_return(self, frame, return_value):
        if isinstance(return_value, TraceEntry):
            return_value.line_number = self.last_line
            self.trace.append(return_value)

    def user_line(self, frame):
        self.number_of_total_lines += 1
        if self.number_of_total_lines > MAX_TOTAL_LINES:
            self.trace.append(TraceEntry(
                error='Number of total lines exectuted exceeded limit of {}'.format(MAX_TOTAL_LINES)))
            raise bdb.BdbQuit

        if frame.f_code.co_filename == '<string>':
            # this is executed only if run from the user's actual code
            self.number_of_user_lines += 1
            if self.number_of_user_lines > MAX_USER_LINES:
                self.trace.append(TraceEntry(
                    error='Number of user lines exectuted exceeded limit of {}'.format(MAX_USER_LINES)))
                raise bdb.BdbQuit
            self.last_line = frame.f_lineno

    def user_call(self, frame, argument_list):
        self.numer_of_function_calls += 1
        if self.numer_of_function_calls > MAX_FUNCTION_CALLS:
            self.trace.append(TraceEntry(
                error='Number of function calls exceeded limit of {}'.format(MAX_FUNCTION_CALLS)))
            raise bdb.BdbQuit

    def user_exception(self, frame, exc_info):
        exc_str = str(exc_info[1]) if len(
            str(exc_info[1])) != 0 else str(exc_info[0])
        self.trace.append(TraceEntry(error=exc_str))
        raise bdb.BdbQuit


def main():
    codestr = sys.stdin.read()
    tracer = Tracer()
    tracer.execute(codestr, __builtins__)
    print(json.dumps(tracer.trace, cls=TraceEntryJSONEncoder))


if __name__ == '__main__':
    main()
