import bdb
from tracer_entry import TraceEntry
import sandbox

class Tracer(bdb.Bdb):

	def __init__(self):
		bdb.Bdb.__init__(self)
		self.trace = []

	# main function
	# it executes the code and returns the trace
	def execute(self, code_str):
		self.trace = []
		sandbox.set_resource_limits()
		safe_globals = sandbox.safe_globals(__builtins__)
		try:
			self.run(code_str, safe_globals, safe_globals)
		except Exception as e:
			print("THIS SHOULD NOT BE EXECUTING. found exception:", e)
		return self.trace
		
			
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
		print("caught user exception:", exc_info[1])
		error_entry = TraceEntry()
		error_entry.error = exc_info[1]
		self.trace = [error_entry]
		raise bdb.BdbQuit

if __name__ == '__main__':
	tracer = Tracer()
	code = open("example.py").read()
	trace = tracer.execute(code)
	for trace_entry in trace:
		trace_entry.display()
		print(' ')