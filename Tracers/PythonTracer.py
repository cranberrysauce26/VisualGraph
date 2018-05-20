import bdb

# for frame and code docs: https://docs.python.org/2/reference/datamodel.html#types
# for bdb docs: https://docs.python.org/2/library/bdb.html
class PythonTracer(bdb.Bdb):

    # constant

    def __init__(self):
        bdb.Bdb.__init__(self)

    # main functionn
    # it executes the code and returns the trace
    def execute(self, code_str):
        self.trace = []
        self.run(code_str)

    def create_trace_entry(self, frame):
        pass

    def user_call(self, frame, argument_list):

        print("user_call in file", frame.f_code.co_filename, "with function", frame.f_code.co_name)
        function_name = frame.f_code.co_name
        prev_line = self.get_stack(frame, None)[0][-2][1]
        trace_entry = (function_name, prev_line)
        print(trace_entry)

        # # why is argument_list null?
        # function_name = frame.f_code.co_name or "<unknown>"
        # argcount = frame.f_code.co_argcount
        # local_variables = frame.f_code.co_varnames
        # # print("calling func", function_name)
        # # dump(self.get_stack(frame,None)[0])
        # # print("calling function", function_name, "with argument_list", argument_list, "and argcount", argcount, "arguments and vars", local_variables, "stack", self.get_stack(frame, None))
        # # print("\n")
        # print("calling function", function_name, ". stack:", self.get_stack(frame,None), "\n\n")

    def user_line(self, frame):
        pass

    # def user_line(self, frame):
    #     line_number = frame.f_lineno
    #     function_name = frame.f_code.co_name or "<unknown>"
    #     # print("executing line", line_number, "co_name", function_name, "locals", frame.f_locals, "stack", self.get_stack(frame, None))
    #     # print("\n")
    #     print("executing line", line_number,".\nstack:", self.get_stack(frame,None), "\nlocal\n", frame.f_code.co_varnames, "\n\n") #global:", frame.f_globals, "\n\n")

    def user_return(self, frame, return_value):
        pass
        # function_name = frame.f_code.co_name or "<unknown>"
        # print("returning from function", function_name, return_value,". curframe,", frame, ", stack:", self.get_stack(frame,None),"\n\n")

    def user_exception(self, frame, exc_info):
        pass

    def do_clear(self, arg):
        pass

tracer = PythonTracer()

code = open("example.py").read()
tracer.execute(code)