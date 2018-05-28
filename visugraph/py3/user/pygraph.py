from trace_entry import add_trace_entry
import random

class Vertex(dict):
    def __init__(self, id, graph):
        object.__setattr__(self, '_graph', graph)
        self.__setitem__('id', id)

    def __getattr__(self, name):
        return self.__getitem__(name)

    def __setattr__(self, name, value):
        if name not in dir(self):
            self.__setitem__(name, value)
            add_trace_entry(
                command_name='set_vertex_property',
                graph_type=self._graph.graph_type,
                graph_id=self._graph.id,
                args=[self.id, name, value]
            )
        else:
            raise(Exception('You are not supposed to set property {0} of {1}'.format(name, self.__class__)))

class Graph:
    def __init__(self, n=0, directed=False, weighted=False):
        object.__setattr__(self, '_property_dict', {})
        object.__setattr__(self, 'id', random.randint(0, 1000000000000000000))
        object.__setattr__(self, 'num_vertices', n)
        object.__setattr__(self, 'directed', directed)
        object.__setattr__(self, 'weighted', weighted)
        object.__setattr__(self, 'graph_type', 'graph')
        object.__setattr__(self, 'vertices', {id:Vertex(id, self) for id in range(1, n+1)})
        object.__setattr__(self, 'adj', {id:list() for id in range(1, n+1)})

        add_trace_entry(
            command_name='construct',
            graph_type=self.graph_type,
            graph_id=self.id,
            args=[n, directed, weighted]
        )

    def add_vertex(self, id=None):
        object.__setattr__(self, 'num_vertices', self.num_vertices+1)
        if id==None:
            id = self.num_vertices
        self.vertices[id] = Vertex(id, self)
        self.adj[id] = list()
        add_trace_entry(
            command_name='add_vertex',
            graph_type=self.graph_type,
            graph_id=self.id,
            args=[id]
        )

    def add_edge(self, u, v, w=1):
        self.adj[u].append((v, w))
        if not self.directed:
            self.adj[v].append((u, w))
        add_trace_entry(
            command_name='add_edge',
            graph_type=self.graph_type,
            graph_id=self.id,
            args=[u, v, w]
        )

    def vertex(self, id):
        return self.vertices[id]

    # provides access to vertex using subscript notation
    # e.g., u = g[5] is equivalent to u = g.vertex(5)
    def __getitem__(self, id):
        return self.vertex(id)
    
    def __getattr__(self, name):
        return self._property_dict[name]

    # provides access to custom graph properties
    def __setattr__(self, name, value):
        if name not in dir(self):
            self._property_dict[name] = value
            add_trace_entry(
                command_name='add_graph_property',
                graph_type=self.graph_type,
                graph_id=self.id,
                args=[name, value]
            )
        else:
            raise(Exception('You are not supposed to set property {0} of {1}'.format(name, self.__class__)))

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
        print('visiting {0}'.format(g.vertex(u).id))
        for v in g.adj[u]:
            if not g[v].visit:
                dfs(v, g)

    for u in g.vertices:
        if not g[u].visit:
            dfs(u, g)
