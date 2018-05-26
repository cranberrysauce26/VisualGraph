# VisualGraph
An interactive graph visualizer.
<<<<<<< HEAD

# How it works so far:

=======
# How it works
The purpose of this project is to let users write code online to interact with a graph interface. For example, users will be able to write in python

    g = Graph(5)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    for v in g.vertic# VisualGraph
An interactive graph visualizer.
# How it works
The purpose of this project is to let users write code online to interact with a graph interface and visualize it. For example, users will be able to write in python

    g = Graph(5)
    g.add_edge(1, 2)
    g.add_edge(2, 3)
    g.add_edge(3, 4)
    for v in g.vertices:
        g[v].visit = False
    def dfs(u, g):
        g[u].visit = True
        g[u].set_color("red")
        for v in g.adj[u]:
            if not g[v].visit:
                dfs(v, g)
    for v in g.vertices:
        if not g[v].visit:
            dfs(v, g)
  
     
Then on the website, they will see a simple dfs function that highlights nodes red when they visit. This is useful for debugging and also learning basic graph theory.
# Working on
# new backend

 - User submits json object to /trace containing the properties `code` which is just the user's code as a string, and `lang` which is the user's coding language.
 - The route simply returns the output of some function (say `get_trace_as_json`) with inputs `code` and `lang`
 - Inside of this function, you generate a `submission_id` which will uniquely identify the current submission
 - Create a folder `/tmp/sub_{submission_id}` Copy the code to `/tmp/sub_{submission_id}/code.in`.  Create an empty file `/tmp/sub_{submission_id}/trace.json`.
 - Find the executable file you can run to trace your user's code. For example, currently to trace python3 code, you can run tracer.py. 
 - Run this executable from `sandbox` , passing `/tmp/sub_{submission_id}/code.in` as stdin and `/tmp/sub_{submission_id}/trace.json` as stdout. It's the tracer's job to read the code from standard input and output the trace to standard output.
 - After `sandbox` is finished running, read the trace as json from `/tmp/sub_{submission_id}/trace.json`, erase the temporary folder, and return this json string.

**Multiple language support**

 - python3 is already implemented
 - python2 can almost be copied from python3
 - TODO: flexible languages like javascript and ruby
 - TODO: semi flexible langauges like java and c sharp can probably have an interface that relies on reflection to determine variables in the node? This will be complex...
 - TODO: compiled langauges. i dunno. Maybe use templates in c++ and overwride a virtual function to_json()?

# What we have right now
We have two pretty much independent parts. There's the backend, written in python, and the front end, written in javascript. All js files are in the folder /static. 

# Backend
To run the backend, either type in the project root directory

    flask run
    or
    python app.py
    
The file app.py runs the server at localhost:5000. So just go to chrome or firefox or whatever and go to the url: localhost:5000. Then you should see the file index.html and a textbox to enter code.

We're using Flask. app.py is pretty much the same as the helloworld flask app in every online tutorial. The main things are 1) GET requests to "/" go to index.html and 2) POST requests to "/trace" send json objects to the server which contains the property "code" which is just the user's code as a string and the response is an array of trace_entries, representing commands. For example, you could get the array as something like 

    [
	   { 
		   "command_name": "construct",
		   "graph_type": "graph",
		   "graph_id": 1234567891011,
		   "args": [13],
		   "return_value": null,
		   "line_number": 5,
		   "error": null
	   },
	   { 
		   "command_name": "add_vertex",
		   "graph_type": "graph",
		   "graph_id": 1234567891011,
		   "args": [666],
		   "return_value": null,
		   "line_number": 6,
		   "error": null
	   },
	   { 
		   "command_name": "add_edge",
		   "graph_type": "graph",
		   "graph_id": 1234567891011,
		   "args": [1, 666],
		   "return_value": null,
		   "line_number": 10,
		   "error": null
	   },
	]

This corresponds to the following operations:
1. Create a graph with id = 12345...11 and with 13 nodes (since the args of "construct" was 13). By default, the nodes have id's {1, 2, 3, ..., 13}. This is called on line number 5 of the user's code and returns no errors.
2. Add a vertex with id 666 to the graph
3. Add an edge between vertices with id 1 and id 666.

From here, the front end handles actually drawing these commands for the user.

Anyways, after getting the POST to /trace, we call the function `get_trace_as_json(code, __builtins__)`.
This returns the trace of the code as a json object (an array of `trace_entry` objects)

So the above function is located in tracer.py. This is (currently) the class that does the real work. It defines the class `Tracer(bdb.Bdb)`. It inherits from bdb.Bdb, which is python's debugger base class. https://docs.python.org/2/library/bdb.html
The important things in this class are 
1. you can run a string of python code with global and local variables you specifiy using the inherited method of Bdb`self._run(code_as_a_string, global_properties, local_properties)`
2. `user_return` is called on every function return. We only need to know when the user calls something in graph cuz that's what we're gonna pass back to the front end. So we do something slightly sketchy. We expose a class Graph in the user's global variables (this is done in sandbox.py). Then in the implementation of graph, whenever we do something like add an edge or add a vertex etc., we return a `trace_entry` object with data like the graph's id, the edge to add or the vertex to add, etc. See tracer_entry.py for more info. Then in Tracer's method user_return, we check if the return value is an instance of trace_entry. If it is, we add it to the `trace` variable, which is just an array of trace_entries. Then once we're done, we return the trace as a json string.

# Frontend

TODO
es:
        g[v].visit = False
    def dfs(u, g):
        g[u].visit = True
        g[u].set_color("red")
        for v in g.adj[u]:
            if not g[v].visit:
                dfs(v, g)
    for v in g.vertices:
        if not g[v].visit:
            dfs(v, g)
  
     
Then on the website, they will see a simple dfs function that highlights nodes red when they visit. This is useful for debugging and also learning basic graph theory.

# Right Now
We have two pretty much independent parts. There's the backend, written in python, and the front end, written in javascript. All js files are in the folder /static. 

# Backend
To run the backend, either type in the project root directory

    flask run
    or
    python app.py
    
The file app.py runs the server at localhost:5000. So just go to chrome or firefox or whatever and go to the url: localhost:5000. Then you should see the file index.html and a textbox to enter code.

We're using Flask. app.py is pretty much the same as the helloworld flask app in every online tutorial. The main things are 1) GET requests to "/" go to index.html and 2) POST requests to "/trace" send json objects which contains the property "code" which is just the user's code as a string. In the future, we would probably also pass the user's langauge as well.

From the POST handler in app.py, we call the function `get_trace_as_json(code, __builtins__)`.
This returns the trace of the code as a json object (an array of `trace_entry` objects)

So the above function is located in tracer.py. This is (currently) the class that does the real work. It defines the class `Tracer(bdb.Bdb)`. It inherits from bdb.Bdb, which is python's debugger base class. https://docs.python.org/2/library/bdb.html
The important things in this class are 1) you can run a string of python code with global and local variables you specifiy using the inherited method of Bdb`self._run(code_as_a_string, global_properties, local_properties)`, 2) `user_return` is called on every function return. We only need to know when the user calls something in graph cuz that's what we're gonna pass back to the front end. So we do something slightly sketchy. We expose a class Graph in the user's global variables (this is done in sandbox.py). Then in the implementation of graph, whenever we do something like add an edge or add a vertex etc., we return a `trace_entry` object with data like the graph's id, the edge to add or the vertex to add, etc. See tracer_entry.py for more info. Then in Tracer's method user_return, we check if the return value is an instance of trace_entry. If it is, we add it to the `trace` variable, which is just an array of trace_entries. Then once we're done, we return the trace as a json string.

# Frontend

TODO
>>>>>>> d5466ef8a011cd4d0f5d58ae0803f75ae7dc2e08
