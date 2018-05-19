import bdb
def dump(obj):
  for attr in dir(obj):
    print("obj.%s = %r" % (attr, getattr(obj, attr)))
# for frame and code docs: https://docs.python.org/2/reference/datamodel.html#types
# for bdb docs: https://docs.python.org/2/library/bdb.html
class PythonTracer(bdb.Bdb):

    def __init__(self):
        bdb.Bdb.__init__(self)

    # main function
    # it executes the code and returns the trace
    def execute(self, code_str):
        pass

    def create_trace_entry(self, frame):
        pass

    def user_call(self, frame, argument_list):
        # why is argument_list null?
        function_name = frame.f_code.co_name or "<unknown>"
        argcount = frame.f_code.co_argcount
        local_variables = frame.f_code.co_varnames
        # print("calling func", function_name)
        # dump(self.get_stack(frame,None)[0])
        # print("calling function", function_name, "with argument_list", argument_list, "and argcount", argcount, "arguments and vars", local_variables, "stack", self.get_stack(frame, None))
        # print("\n")
        print("calling function. stack:", self.get_stack(frame,None), "\n\n")

    def user_line(self, frame):
        line_number = frame.f_lineno
        function_name = frame.f_code.co_name or "<unknown>"
        # print("executing line", line_number, "co_name", function_name, "locals", frame.f_locals, "stack", self.get_stack(frame, None))
        # print("\n")
        print("executing line", line_number,". stack:", self.get_stack(frame,None), "\n\n")

    def user_return(self, frame, return_value):
        function_name = frame.f_code.co_name or "<unknown>"
        print("returning from function", function_name, return_value,".stack:", self.get_stack(frame,None),"\n\n")

    def user_exception(self, frame, exc_info):
        pass

    def do_clear(self, arg):
        pass

tracer = PythonTracer()

code = open("example.py").read()
tracer.run(code)