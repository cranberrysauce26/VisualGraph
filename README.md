
# VisualGraph
An interactive graph visualizer.
# Overview
The purpose of this project is to let users write code online to interact with a graph interface and visualize it. For example, users will be able to write in python

    g = Graph(5)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    for v in g.vertices:
        g[v].visit = False
    def dfs(u, g):
        g[u].visit = True
        for v in g.adj[u]:
            if not g[v].visit:
                dfs(v, g)
    for v in g.vertices:
        if not g[v].visit:
            dfs(v, g)
  
     
Then on the website, they will see a simple dfs function where each vertex has a property above it called `visit` that begins as `False` and is set to `True` when it is reached by the dfs. This is useful for debugging and also learning basic graph theory.

# How it works
 - Frontend submits json object to /trace containing the properties `code` which is the user's code as a string, and `lang` which is the user's coding language.
 - Backend returns the trace, which is the sequence of commands the user's code tells to our graph interface. For example, if the user creates a graph with 5 vertices and adds an edge between vertices 1 and 2, the trace would conceptually be `["Create a graph with 5 vertices", "Add an edge between vertices 1 and 2"]`
 - Front end takes this trace and animates it in the browser

# An example of trace

    g = Graph(5)
    g.add_edge(1, 2)
    g.vertex(2).happy = True

   The above code generates the following trace.


    [
	    {
		    "command_name": "construct", 
		    "graph_type": "graph", 
		    "graph_id": 0, 
		    "args": [5, false, false, "Graph 0"],
		    "return_value": null, 
		    "line_number": 1, 
		    "error": null
	    }, 
	    {
		    "command_name": "add_edge", 
		    "graph_type": "graph", 
		    "graph_id": 0, 
		    "args": [1, 2, 1], 
		    "return_value": null, 
		    "line_number": 2, 
		    "error": null
		 },
	 {
		  "command_name": "set_vertex_property",
		  "graph_type": "graph",
		  "graph_id": 0,
		  "args": [2, "happy", true],
		  "return_value": null,
		  "line_number": 3,
		  "error": null
	}
	]
# How is the trace generated?
 - The user's code is copied to a temporary folder `project_root/tmp/{random_uuid}`. This is handled by `BaseRunner`.
 - We have a `Tracer` class which inherits from python's builtin `BDB` debugger class. This class allows us to track many things. Specifically, it allows us to detect whenever a function is returned and get things like the line number, the function name, and the return value. So the trick is to return a `TraceEntry` object at the end of each `Graph` method, which describes what the method is doing. Then, using the `Tracer` class, we check if the return value has type `TraceEntry`. If so, we receive this `TraceEntry` object and add it to a list.
 - If run as main, `tracer.py` takes the code from standard input and outputs the trace as a json string to standard output. We use a sandboxed environment with access to our `Graph` class to run `tracer.py` with the code as standard input. We then return the standard output.

# How does sandboxing work?
 - There are two levels of sandboxing.
 - The first is `pybox.py`, which disables certain dangerous modules like `os` and `sys`. It also redefines `print` to another method which mirrors `print` exactly except that it doesn't actually print anything, but instead returns a `TraceEntry` object saying that the user tried to print something.
 - `pybox.py` also makes the `Graph` class a global variable for the code that `Tracer` is running to access.
 - Finally, `pybox.py` makes sure that any attempt to access illegal functions is recorded as a `TraceEntry` object saying that this module or function is illegal.
 - The second level of sandboxing is Linux's seccomp. This is only available for Linux machines, and the seccomp library must be downloaded first.
 - See `seccomp.c` for details. All it does is disable dangerous syscalls.

**Multiple language support**

 - python3 is already implemented
 - python2 can almost be copied from python3
 - TODO: flexible languages like javascript and ruby
 - TODO: semi flexible languages like java and C# can probably be implemented as well.
