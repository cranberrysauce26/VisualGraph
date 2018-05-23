// TODO: Add exception handling for invalid traces

class Graph{
    static graphs = {}; // a dictionary mapping ids to graphs

    static CallFunction(trace){
        if (trace["error"]){
            return;
        }
        var name = trace["command_name"];
        var args = trace["args"];
        var id = trace["graph_id"];
        var retVal = trace["rturn_value"];
        var line = trace["line_number"];

        if (name == "construct"){
            if (args.length == 0) {
                graphs[id] = new Graph();
            }
            else {
                graphs[id] = new Graph(args[0]);
            }
        }
        else if (name == "add_vertex"){
            graphs[id].add_vertex();
        }
        else if (name == "add_edge") {
            graphs[id].add_edge(args[0], args[1]);
        }
        else {
            // Error: invalid command
            return;
        }
    }

    constructor(n=0){
        this.n = n;
        this.adj = {};
        for (i = 1; i <= n; i++){
            this.adj[i] = {};
        }
    }

    add_vertex(){
        this.n++;
        this.adj[n] = {};
    }

    add_edge(u, v) {
        if (u > 0 && u <= this.n && v > 0 && v <= this.n){
            this.adj[u][v] = 1;
        }
        else {
            // Error: this should be happenning
            return;
        }
    }
}
