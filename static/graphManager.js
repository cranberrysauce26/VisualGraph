class GraphManager {
    constructor() {
        this.graphs = {}; // stores the history of each graph
        this.edits = {}; // keeps track of the line number of each edit
        // edits[g][i] is the line number of the i-th edit made to graph g
        // graphs[g][i] is what the graph looks like after that edit was made
    }

    callFunction(trace) {
        if (trace["error"]) {
            return;
        }
        var name = trace["command_name"];
        var args = trace["args"];
        var id = trace["graph_id"];
        var retVal = trace["rturn_value"];
        var line = trace["line_number"];
        if (name == "construct") {
            if (args.length != 4) {
                alert("Error: Wrong number of arguments for graph constructor");
                return;
            }
            this.graphs[id] = new Array();
            this.edits[id] = new Array();
            this.graphs[id].push(new Graph(args[0], args[1], args[2], args[3]));
            this.edits[id].push(line);
        }
        else if (name == "add_vertex") {
            var copy = this.graphs[id][this.graphs[id].length - 1].copy(); // current version of the graph
            copy.addVertex();
            this.graphs[id].push(copy);
            this.edits[id].push(line);
        }
        else if (name == "add_edge") {
            if (args.length != 3) {
                alert("Error: Wrong number of arguments for add_edge");
                return;
            }
            var copy = this.graphs[id][this.graphs[id].length - 1].copy(); // current version of the graph
            copy.addEdge(args[0], args[1], args[2]);
            this.graphs[id].push(copy);
            this.edits[id].push(line);
        }
        else if (name == "set_vertex_property") {
            if (args.length != 3) {
                alert("Error: Wrong number of arguments for setting vertex prooperty");
                return;
            }
            var copy = this.graphs[id][this.graphs[id].length - 1].copy(); // current version of the graph
            copy.vertices[args[0]].setProperty(args[1], args[2]);
            this.graphs[id].push(copy);
            this.edits[id].push(line);
        }
        else {
            alert("Error: Invalid command name: " + command_name);
            return;
        }
    }

    displayAll(line) {
        for (var id in this.graphs) { // will order of IDs change?
            for (var i = this.edits[id].length - 1; i >= 0; i--) {
                if (this.edits[id][i] <= line) { // Do we want it to be <=, or < ?
                    this.graphs[id][i].displayVis();
                    break;
                }
            }
        }
    }
}
