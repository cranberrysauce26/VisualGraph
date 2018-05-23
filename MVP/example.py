from graph import Graph
g = Graph(4)
g.add_edge(1, 2)
g.add_edge(2, 1)
g.add_vertex();
g.add_edge(5, 1)
# g.add_vertex(5)
# g.add_edge(1, 2)
# g.add_edge(2, 1)
# g.add_edge(1, 4)
# g.add_edge(4, 1)
# for u in g.vertices:
#     g[u].visit = False

# def dfs(u, g):
#     g[u].visit = True
#     print("visiting {0}".format(g.vertex(u).id))
#     for v in g.adj[u]:
#         if not g[v].visit:
#             dfs(v, g)

# for u in g.vertices:
#     if not g[u].visit:
#         dfs(u, g)
