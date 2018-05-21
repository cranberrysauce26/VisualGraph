import bdb
from tracer_entry import TraceEntry
import sandbox

class Tracer(bdb.Bdb):

    def __init__(self):
        bdb.Bdb.__init__(self)
        self.trace = []

    # main function
    # it executes the code and returns the trace
    def execute(self, code_str, builtins=__builtins__):
        self.trace = []
        # This causes errors for me!?!
        # sandbox.set_resource_limits()
        safe_globals = sandbox.safe_globals(builtins)
        try:
            self.run(code_str, safe_globals, safe_globals)
        except Exception as e:
            trace_entry = TraceEntry()
            trace_entry.error = str(e)
            self.trace = [trace_entry]
            

    def user_return(self, frame, return_value):
        if isinstance(return_value, TraceEntry):
            # TODO: Make this less sketchy, maybe by iterating over the linked list
            prev_frame = frame.f_back.f_back
            assert(prev_frame)
            return_value.line_number = prev_frame.f_lineno
            self.trace.append(return_value)

    def user_line(self, frame):
        pass

    def user_call(self, frame, argument_list):
        pass

    def user_exception(self, frame, exc_info):
        error_entry = TraceEntry()
        error_entry.error = exc_info[1]
        self.trace = [error_entry]
        raise bdb.BdbQuit

if __name__ == '__main__':
    tracer = Tracer()
    code = open("example.py").read()
    tracer.execute(code, __builtins__)
    trace = tracer.trace
    print("\nhere is the trace:")
    for i, trace_entry in enumerate(trace):
        print('trace[{0}]: '.format(i), end='')
        trace_entry.display()
        print(' ')