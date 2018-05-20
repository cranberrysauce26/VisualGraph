from graph import Graph


class C1:
	pass

c = C1()
if isinstance(c, C1):
	print("yay")

def do_something():
	for i in range(1, 10):
		gr = Graph(i)
		gr.add_vertice()

g = Graph(2)
g.add_vertice()
g.add_edge(2, 3)
g2 = Graph(5)
g2.add_edge(1, 5)
# print(dir(g.add_vertice))
# print(g.add_vertice.interface_method)
do_something()
