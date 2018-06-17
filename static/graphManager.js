class GraphManager {
    constructor() {
        this.graphs = {};
    }

    callFunction(trace){
        if (trace["error"]){
            return;
        }
        var name = trace["command_name"];
        var args = trace["args"];
        var id = trace["graph_id"];
        var retVal = trace["rturn_value"];
        var line = trace["line_number"];
        if (name == "construct"){
            if (args.length != 3){
                alert("Error: Wrong number of arguments for graph constructor");
                return;
            }
            this.graphs[id] = new Graph(args[0], args[1], args[2]);
        }
        else if (name == "add_vertex"){
            this.graphs[id].addVertex();
        }
        else if (name == "add_edge") {
            if (args.length != 3){
                alert("Error: Wrong number of arguments for add_edge");
                return;
            }
            this.graphs[id].addEdge(args[0], args[1], args[2]);
        }
        else if (name == "set_vertex_property") {
            if (args.length != 3){
                alert("Error: Wrong number of arguments for setting vertex prooperty");
                return;
            }
            this.graphs[id].vertices[args[0]].setProperty(args[1], args[2]);
        }
        else {
            alert("Error: Invalid command name: "+command_name);
            return;
        }
    }

    displayAll(){
        for (var id in this.graphs){
            this.graphs[id].displayVis();
        }
    }
}
