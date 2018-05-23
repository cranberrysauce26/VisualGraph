import bdb
import json
from tracer_entry import TraceEntry, TraceEntryJSONEncoder
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
            self.trace.append(TraceEntry(error=str(e)))


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
        self.trace.append(TraceEntry(error=str(exc_info[1])))
        raise bdb.BdbQuit

def get_trace_as_json(code_str, builtins = __builtins__):
    tracer = Tracer()
    tracer.execute(code_str, builtins)
    print(tracer.trace)
    return json.dumps(tracer.trace, cls=TraceEntryJSONEncoder)

if __name__ == '__main__':
    print("Running...")
    tracer = Tracer()
    import sys
    code = open("example.py").read()
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
