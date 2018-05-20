import bdb
from tracer_entry import TraceEntry

class Tracer(bdb.Bdb):
	def __init__(self):
		bdb.Bdb.__init__(self)
		self.GRAPH_IMPLEMENTATION_FILE = self.canonic("graph.py")

	# main function
	# it executes the code and returns the trace
	def execute(self, code_str):
		self.trace = []
		self.run(code_str)
		return self.trace

	def user_return(self, frame, return_value):

		if isinstance(return_value, TraceEntry):
			print("YES")
			prev_frame = frame.f_back
			assert(prev_frame)
			return_value.line_number = prev_frame.f_lineno
			self.trace.append(return_value)

	def user_line(self, frame):
		pass

	def user_call(self, frame, argument_list):
		pass

	def user_exception(self, frame, exc_info):
		pass

if __name__ == '__main__':
	tracer = Tracer()
	code = open(tracer.canonic("example.py")).read()
	trace = tracer.execute(code)
	for trace_entry in trace:
		print("trace on graph with id", trace_entry.graph_id,"with function_name", trace_entry.command_name, "line number", trace_entry.line_number, "and args: ", end='')
		for arg in trace_entry.args:
			print(arg, end=' ')
		print()
	print("type of trace entry is", type(TraceEntry()))