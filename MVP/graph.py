from tracer_entry import TraceEntry

class Graph:
	num_graphs=0

	def _trace___init__(self, n):
		tracer_entry = TraceEntry()
		tracer_entry.graph_id = self.id
		tracer_entry.args = [n]
		tracer_entry.return_value = None
		tracer_entry.command_name = "construct"

	def _trace_add_vertice(self):
		tracer_entry = TraceEntry()
		tracer_entry.graph_id = self.id
		tracer_entry.args = []
		tracer_entry.return_value = None
		tracer_entry.command_name = "add_vertice"
		return tracer_entry

	def _trace_add_edge(self, u, v):
		tracer_entry = TraceEntry()
		tracer_entry.graph_id = self.id
		tracer_entry.args = [u, v]
		tracer_entry.return_value = None
		tracer_entry.command_name = "add_edge"
		return tracer_entry

	def __init__(self, n=0):
		Graph.num_graphs = Graph.num_graphs + 1
		self.id = Graph.num_graphs
		self.n = n
		self.adj = {i:{} for i in range(1, n+1)}
		self._trace___init__(n)

	def add_vertice(self):
		self.n = self.n + 1
		self.adj[self.n] = dict()
		self._trace_add_vertice()

	def add_edge(self, u, v):
		self.adj[u][v]=1
		self._trace_add_edge(u, v)

if __name__ == '__main__':
	# print(PYTHONPATH)
	tr = TraceEntry()
	print(type(tr))
	print(isinstance(tr, TraceEntry))