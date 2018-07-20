class Graph {
    constructor(n, directed, weighted, name) {
        this.n = n; // number of vertices
        this.directed = directed; // Boolean: whether graph is directed
        this.weighted = weighted; // Boolean: whether graph is weighted
        this.name = name; // String: name of graph
        this.vertices = {}; // map from vertex ID to vertex object
        this.adj = {}; // map from vertex ID to a list of edges
        for (var i = 1; i <= this.n; i++) {
            this.vertices[i] = new Vertex(i, this);
            this.adj[i] = {}; // map from vertices connected to i, to weights of that edge (Replace weight with edge class?)
        }
    }

    // copy constructor
    constructor(g) {
        this.n = g.n;
        this.directed = g.directed;
        this.weighted = g.weighted;
        this.name = g.name;
        this.vertices = {};
        this.adj = {};
        for (var id in g.vertices) {
            this.vertices[id] = new Vertex(g.vertices[id]);
            this.vertices[id].graph = this;
            for (var neighbor in g.adj[id]) {
                this.adj[id][neighbor] = g.adj[id][neighbor]; // replace with edge copy constructor
            }
        }
    }

    // TODO: add_vertex with id
    addVertex() {
        this.n++;
        this.adj[this.n] = {};
        this.vertices[this.n] = new Vertex(this.n, this);
    }

    addEdge(u, v, w) {
        if (u > 0 && u <= this.n && v > 0 && v <= this.n) {
            this.adj[u][v] = w;
            if (!this.directed) {
                this.adj[v][u] = w;
            }
        }
        else {
            alert("Error: Attempted to create invalid edge");
            return;
        }
    }

    displayVis() {
        var nodeArray = new Array();
        var edgeArray = new Array();
        for (var i = 1; i <= this.n; i++) {
            nodeArray.push({
                id: this.vertices[i].id,
                label: this.vertices[i].id.toString(),
                color: this.vertices[i].properties['color']
            });
            for (var j in this.adj[i]) {
                if (!this.directed && j < i) // in undirected graphs, make sure each edge is just displayed once
                    continue;
                edgeArray.push({ from: i, to: j });
            }
        }
        var nodes = new vis.DataSet(nodeArray);
        var edges = new vis.DataSet(edgeArray);

        var container = document.getElementById('mynetwork');
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {};

        var network = new vis.Network(container, data, options);
    }
}
