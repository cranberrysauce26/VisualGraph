from graph import Graph

def do_something():
	for i in range(1, 10):
		gr = Graph(i)
		gr.add_vertice(i)

g = Graph(2)
g.add_edge(1, 2)
g.add_edge(2, 3)
g2 = Graph(5)
g2.add_edge(1, 5)
g.edge_exists(1, 2)
do_something()
