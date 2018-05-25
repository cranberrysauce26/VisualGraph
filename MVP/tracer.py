import bdb
import json
from tracer_entry import TraceEntry, TraceEntryJSONEncoder
import sandbox

MAX_LINES = 300
MAX_FUNCTION_CALLS = 300

class Tracer(bdb.Bdb):

    def __init__(self):
        bdb.Bdb.__init__(self)
        self.trace = []
        self.last_line = -1
        self.number_of_lines = 0
        self.numer_of_function_calls = 0

    # main function
    # it executes the code and returns the trace
    def execute(self, code_str, builtins=__builtins__):
        self.trace = []
        # This causes errors for me!?!
        sandbox.set_resource_limits()
        safe_globals = sandbox.safe_globals(builtins)
        try:
            self.run(code_str, safe_globals, safe_globals)
        except Exception as e:
            print("caught run exception ", e)
            self.trace.append(TraceEntry(error=str(e)))
            # raise bdb.BdbQuit


    def user_return(self, frame, return_value):
        if isinstance(return_value, TraceEntry):
            # TODO: Make this less sketchy, maybe by iterating over the linked list
            return_value.line_number = self.last_line
            self.trace.append(return_value)

    def user_line(self, frame):
        self.number_of_lines += 1
        if self.number_of_lines > MAX_LINES:
            self.trace.append(TraceEntry(error="Number of lines exectuted exceeded limit of {}".format(MAX_LINES)))
            raise bdb.BdbQuit

        if frame.f_code.co_filename == '<string>':
            self.last_line = frame.f_lineno

    def user_call(self, frame, argument_list):
        self.numer_of_function_calls += 1
        if self.numer_of_function_calls > MAX_FUNCTION_CALLS:
            self.trace.append(TraceEntry(error="Number of function calls exceeded limit of {}".format(MAX_FUNCTION_CALLS)))
            raise bdb.BdbQuit

    def user_exception(self, frame, exc_info):
        exc_str = str(exc_info[1]) if len(str(exc_info[1])) != 0 else str(exc_info[0])
        print("caught user exception", exc_str)
        self.trace.append(TraceEntry(error=exc_str))
        raise bdb.BdbQuit

def get_trace_as_json(code_str, builtins = __builtins__):
    tracer = Tracer()
    tracer.execute(code_str, builtins)
    print("returning from get_trace_as_json",json.dumps(tracer.trace, cls=TraceEntryJSONEncoder))
    return json.dumps(tracer.trace, cls=TraceEntryJSONEncoder)

if __name__ == '__main__':
    print("Running...")
    tracer = Tracer()
    import os
    code = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "example.py")).read() # for everyone
    print("filename is", os.path.join(os.path.dirname(os.path.abspath(__file__)), "example.py"))
	# code = open("/home/howard/Documents/VisualGraph/MVP/example.py").read() # for Howard
    tracer.execute(code, __builtins__)
    trace = tracer.trace
    print("\nhere is the trace:")
    for i, trace_entry in enumerate(trace):
        print('trace[{0}]: '.format(i), end='')
        trace_entry.display()
        print(' ')

# tracer = Tracer()
# code = request.data["code"]
# tracer.execute(code, __builtins__)
# trace = tracer.trace
# str "Traces Done"
# return Response(str)
