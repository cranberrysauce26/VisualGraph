import bdb

class PythonTracer(bdb.Bdb):

    def user_call(self, frame, argument_list):
        # why is argument_list null?
        function_name = frame.f_code.co_name or "<unknown>"
        argcount = frame.f_code.co_argcount
        local_variables = frame.f_code.co_varnames
        print("calling function", function_name, "with argument_list", argument_list, "and argcount", argcount, "arguments and vars", local_variables)
    def user_line(self, frame):
        line_number = frame.f_lineno
        function_name = frame.f_code.co_name or "<unknown>"
        print("executing line", line_number, "co_name", function_name, "locals", frame.f_locals)

    def user_return(self, frame, return_value):
        function_name = frame.f_code.co_name or "<unknown>"
        print("returning from function", function_name, return_value)

    def user_exception(self, frame, exc_info):
        pass
    def do_clear(self, arg):
        pass

tracer = PythonTracer()

code = open("example.py").read()
tracer.run(code)

# code = open("example.py").read()
# db.set_break(db.canonic("example.py"), 6)
# import example
# print(db.get_all_breaks())
# db.run(open("example.py").read())
# db.runcall(example.f, 5)
# dump(db)
