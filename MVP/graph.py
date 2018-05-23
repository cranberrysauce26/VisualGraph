from tracer_entry import TraceEntry

class Vertex(dict):
    def __init__(self, id, graph):
        self._graph = graph
        self.id = id

    def __getattr__(self, name):
        return self.__getitem__(name)
    
    def _trace___setattr__(self, name, value):
        return self._graph._mark_trace_entry(TraceEntry(
            command_name="set_vertex_property",
            args=[name, value]
        ))
    def __setattr__(self, name, value):
        if name == '_graph':
            object.__setattr__(self, name, value)
        elif name not in dir(self):
           self.__setitem__(name, value)
           self._trace___setattr__(name, value)
        else:
            raise(Exception("You are not allowed to set property {0} of {1}".format(name, self.__class__)))

class Graph:

    num_graphs = 0

    def __init__(self, n=0):
        Graph.num_graphs = Graph.num_graphs + 1
        self.id = Graph.num_graphs
        self.num_vertices = n
        self.graph_type = "graph"
        # by default, index by 1, 2, ..., n
        # however, it is flexible. So you can index by strings, etc.
        self.vertices = {id:Vertex(id, self) for id in range(1, self.num_vertices+1)} # vertex list
        self.adj = {id:list() for id in range(1, self.num_vertices+1)} # adjancency list
        self.edges = () # edge list

    def add_vertex(self, id):
        self.vertices[id] = Vertex(id, self)
        self.adj[id] = list()
        self._trace_add_vertex(id)

    def add_edge(self, u, v):
        self.adj[u].append(v)
    
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

    def _trace_add_vertex(self, id):
        return self._mark_trace_entry(TraceEntry(
            command_name="add_vertex",
            args = [id]
        ))
    
    def _trace_add_edge(self, u, v):
        return self._mark_trace_entry(TraceEntry(
            command_name="add_edge",
            args=[u,v]
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
