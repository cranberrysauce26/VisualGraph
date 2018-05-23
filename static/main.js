// TODO: Add exception handling for invalid traces

class Graph{
    constructor(n=0){
        // alert("In graph constructor");
        this.n = n;
        this.adj = {};
        for (var i = 1; i <= this.n; i++){
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

class GraphManager {
    constructor() {
        this.graphs = {};
    }

    CallFunction(trace){
        // alert("In CallFunction");
        if (trace["error"]){
            return;
        }
        var name = trace["command_name"];
        var args = trace["args"];
        var id = trace["graph_id"];
        var retVal = trace["rturn_value"];
        var line = trace["line_number"];
        if (name == "construct"){
            // alert("Making new graph");
            this.graphs[id] = new Graph(args[0]);
            // alert("Done");
        }
        else if (name == "add_vertex"){
            this.graphs[id].add_vertex();
        }
        else if (name == "add_edge") {
            this.graphs[id].add_edge(args[0], args[1]);
        }
        else {
            // Error: invalid command
            return;
        }
    }

    displayAll(){
        document.getElementById("Graphs").innerHTML = "";
        for (var id in this.graphs){
            document.getElementById("Graphs").innerHTML += this.graphs[id].display();
        }
    }
}

var graphManager = new GraphManager();

function Visualize() {
    // alert("Visualize called");
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
            alert(traces.length);
            traces.forEach(function(trace){
                document.getElementById("output").innerHTML += JSON.stringify(trace) + "<br>";
                graphManager.CallFunction(trace);
            });
            document.getElementById("output").innerHTML += "Finished printing traces";
        }
    };
    xhttp.open("POST", "/trace", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(dat));
}
