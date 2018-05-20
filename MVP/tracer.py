import bdb

class TraceEntry:
	pass

class Tracer(bdb.Bdb):
	def __init__(self):
		bdb.Bdb.__init__(self)
		self.GRAPH_IMPLEMENTATION_FILE = self.canonic("graph.py")

    # main functionn
    # it executes the code and returns the trace
	def execute(self, code_str):
		self.trace = []
		self.run(code_str)
		return self.trace

	def user_call(self, frame, argument_list):

		file_name = frame.f_code.co_filename
		function_name = frame.f_code.co_name

		# print("user_call in file", file_name, "with function", function_name)
		if file_name == self.GRAPH_IMPLEMENTATION_FILE:

			prev_frame = frame.f_back
			assert(prev_frame)
			prev_line = prev_frame.f_lineno
			# print(frame.f_locals)
			nargs = frame.f_code.co_argcount-1

			function_args = []
			
			for i in range(1, nargs+1):
				argname = frame.f_code.co_varnames[i]
				argval = frame.f_locals[argname]
				function_args.append(argval)

			trace_entry = TraceEntry()
			trace_entry.function_name = function_name
			trace_entry.line_number = prev_line
			trace_entry.argument_list = function_args
			# trace_entry.graph_id 

			self.trace.append(trace_entry)

	def user_line(self, frame):
		pass

	def user_return(self, frame, return_value):
		pass

	def user_exception(self, frame, exc_info):
		pass

tracer = Tracer()
code = open(tracer.canonic("example.py")).read()
trace = tracer.execute(code)
for trace_entry in trace:
	print("trace with function_name", trace_entry.function_name, "line number", trace_entry.line_number, "and args")
	for arg in trace_entry.argument_list:
		print(arg)