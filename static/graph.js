class Graph {
    constructor(n, directed, weighted){
        this.n = n;
        this.directed = directed;
        this.weighted = weighted;
        this.vertices = {};
        this.adj = {};
        for (var i = 1; i <= this.n; i++){
            this.vertices[i] = new Vertex(i, this);
            this.adj[i] = {};
        }
    }

    // TODO: add_vertex with id
    add_vertex(){
        this.n++;
        this.adj[this.n] = {};
        this.vertices[this.n] = new Vertex(this.n, this);
    }

    add_edge(u, v, w) {
        if (u > 0 && u <= this.n && v > 0 && v <= this.n){
            this.adj[u][v] = w;
            if (!this.directed){
                this.adj[v][u] = w;
            }
        }
        else {
            alert("Error: Attempted to create invalid edge");
            return;
        }
    }

    displayVis(){
        var nodeArray = new Array();
        var edgeArray = new Array();
        for (var i = 1; i <= this.n; i++){
            nodeArray.push({
                id: this.vertices[i].id,
                label: this.vertices[i].id.toString(),
                color: this.vertices[i].properties['color']
            });
            for (var j in this.adj[i]){
                if (!this.directed && j < i) // in undirected graphs, make sure each edge is just displayed once
                    continue;
                edgeArray.push({from: i, to: j});
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
