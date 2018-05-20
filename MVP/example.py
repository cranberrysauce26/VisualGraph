from graph import Graph

g = Graph(2)
g.add_edge(1, 2)
g.add_edge(2, 3)
g2 = Graph(5)
g2.add_edge(1, 5)
g.edge_exists(1, 2)
