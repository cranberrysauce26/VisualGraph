class Graph:
	num_graphs=0
	def __init__(self, n):
		self.num_graphs = self.num_graphs + 1
		self.id = self.num_graphs
		self.n = n
		self.adj = dict()
		for i in range(1, n+1):
			self.adj[i] = dict()

	def add_vertice(self):
		self.n = self.n + 1
		self.adj[self.n] = dict()

	def add_edge(self, u, v):
		self.adj[u][v]=1

	def edge_exists(self, u, v):
		return self.adj[u][v] != 0