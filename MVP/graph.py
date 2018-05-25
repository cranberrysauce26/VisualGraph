from tracer_entry import TraceEntry
import random
class Vertex(dict):
    def __init__(self, id, graph):
        object.__setattr__(self, '_graph', graph)
        self.__setitem__('id', id)

    def __getattr__(self, name):
        return self.__getitem__(name)

    def _trace___setattr__(self, name, value):
        self._graph._mark_trace_entry(TraceEntry(
            command_name="set_vertex_property",
            args=[self.id, name, value]
        ))
    def __setattr__(self, name, value):
        if name not in dir(self):
           self.__setitem__(name, value)
           self._trace___setattr__(name, value)
        else:
            raise(Exception("You are not allowed to set property {0} of {1}".format(name, self.__class__)))

class Graph:
    def __init__(self, n=0, directed=False, weighted=False):
        self.id = random.randint(0, 1000000000000000000)
        self.num_vertices = n
        self.directed = directed
        self.weighted = weighted
        self.graph_type = "graph"
        # by default, index by 1, 2, ..., n
        # however, it is flexible. So you can index by strings, etc.
        self.vertices = {id:Vertex(id, self) for id in range(1, self.num_vertices+1)} # vertex list
        self.adj = {id:list() for id in range(1, self.num_vertices+1)} # adjancency list
        self.edges = () # edge list
        self._trace___init__(self.num_vertices, self.directed, self.weighted)

    def add_vertex(self, id):
        self.vertices[id] = Vertex(id, self)
        self.adj[id] = list()
        self._trace_add_vertex(id)

    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))
        self._trace_add_edge(u, v, w)

    def vertex(self, id):
        return self.vertices[id]

    # provides access to vertex using subscript notation
    # e.g., u = g[5] is equivalent to u = g.vertex(5)
    def __getitem__(self, id):
        return self.vertex(id)

    def _mark_trace_entry(self, trace_entry):
        trace_entry.graph_id = self.id
        trace_entry.graph_type = self.graph_type
        return trace_entry

    def _trace___init__(self, n, directed, weighted):
        self._mark_trace_entry(TraceEntry(
            command_name="construct",
            args = [n, directed, weighted]
        ))

    def _trace_add_vertex(self, id):
        self._mark_trace_entry(TraceEntry(
            command_name="add_vertex",
            args = [id]
        ))

    def _trace_add_edge(self, u, v, w):
        self._mark_trace_entry(TraceEntry(
            command_name = "add_edge",
            args = [u, v, w]
        ))

if __name__ == '__main__':
    # do a dfs!
    n = int(input())
    m = int(input())
    g = Graph(n)
    for i in range(m):
        u = int(input())
        v = int(input())
        g.add_edge(u, v)
        g.add_edge(v, u)

    for u in g.vertices:
        g[u].visit = False

    def dfs(u, g):
        g[u].visit = True
        print("visiting {0}".format(g.vertex(u).id))
        for v in g.adj[u]:
            if not g[v].visit:
                dfs(v, g)

    for u in g.vertices:
        if not g[u].visit:
            dfs(u, g)
