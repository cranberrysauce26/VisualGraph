// TODO: Add exception handling for invalid traces

class GraphManager {
    constructor() {
        alert("In GraphManager constructor");
        this.graphs = {};
    }

    CallFunction(trace){
        alert("In CallFunction");
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

    displayAll(){
        document.getElementById("Graphs").innerHTML = "";
        for (var id in graphs){
            document.getElementById("Graphs").innerHTML += graphs[id].display();
        }
    }
}

class Graph{
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

    // returns HTML code for the graph display
    display(){
        return "HTML for graph";
    }
}


var graphManager = new GraphManager();

function Visualize() {
    var text = $("#textbox").val();
    var dat = {code : text}
    if (text.length == 0) {
        document.getElementById("output").innerHTML = "You didn't enter anything!";
        return;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("output").innerHTML = "Traces:<br>";
            var str = this.responseText;
            var traces = JSON.parse(str);
            traces.forEach(function(trace){
                document.getElementById("output").innerHTML += JSON.stringify(trace) + "<br>";
                alert("Calling graph manager");
                graphManager.CallFunction(trace);
                alert("Graph manager ");
                document.getElementById("output").innerHTML += "Hi";
            });
        }
    };
    xhttp.open("POST", "/trace", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(dat));
}
