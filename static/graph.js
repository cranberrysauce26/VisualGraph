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

    // copies the graph
    copy() {
        var g = new Graph(this.n, this.directed, this.weighted, this.name);
        g.vertices = {};
        g.adj = {};
        for (var id in this.vertices) {
            g.vertices[id] = this.vertices[id].copy();
            g.vertices[id].graph = g;
            g.adj[id] = {};
            for (var neighbor in this.adj[id]) {
                g.adj[id][neighbor] = this.adj[id][neighbor]; // replace with edge copy
            }
        }
        return g;
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

    displayVis(id) {
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

        var container = document.getElementById(id); // must make sure that graph id does not match any other element id
        var data = {
            nodes: nodes,
            edges: edges
        };
        var options = {};

        var network = new vis.Network(container, data, options);
    }
}
