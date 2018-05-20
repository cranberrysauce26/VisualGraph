class Graph:
	def _visual_build(self, n):
		self.n = n
		self.adj = dict()
		for i in range(1, n+1):
			self.adj[i] = dict()

	def _visual_add_edge(self, u, v):
		self.adj[u][v]=1

	def _visual_add_vertice(self):
		self.n = self.n + 1
		self.adj[self.n] = dict()

	def __init__(self, n):
		self._visual_build(n)

	def add_vertice(self):
		self._visual_add_vertice()

	def add_edge(self, u, v):
		self._visual_add_edge(u, v)

	def edge_exists(self, u, v):
		return self.adj[u][v] != 0
