// TODO: Add exception handling for invalid traces

class Graph{
    constructor(n){
        // alert("In graph constructor");
        this.n = n;
        this.adj = {};
        for (var i = 1; i <= this.n; i++){
            this.adj[i] = {};
        }
    }

    add_vertex(){
        this.n++;
        this.adj[this.n] = {};
    }

    add_edge(u, v) {
        if (u > 0 && u <= this.n && v > 0 && v <= this.n){
            this.adj[u][v] = 1;
        }
        else {
            alert("Error: Attempted to create invalid edge");
            return;
        }
    }

    // returns HTML code for the graph display
    display(){
        var bigR = 100;
        var smallR = 40;
        var center = new paper.Point(200, 200);
        for (var i = 0; i < this.n; i++){
            var angle = 2*i*Math.PI/this.n;
            var shift = new paper.Point(bigR*Math.cos(angle), bigR*Math.sin(angle));
            var vertex = new paper.Path.Circle(center.add(shift), smallR);
            vertex.fillColor = 'blue';
            var text = new paper.PointText(center.add(shift).add(new paper.Point(0,10)));
            text.justification = 'center';
            text.fillColor = 'white';
            text.fontSize = '30px';
            text.content = i;
        }
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
            this.graphs[id] = new Graph(args[0]);
        }
        else if (name == "add_vertex"){
            this.graphs[id].add_vertex();
        }
        else if (name == "add_edge") {
            this.graphs[id].add_edge(args[0], args[1]);
        }
        else {
            alert("Error: Invalid command");
            return;
        }
    }

    displayAll(){
        var canvas = document.getElementById("Display");
        paper.setup(canvas);
        for (var id in this.graphs){
            this.graphs[id].display();
        }
        paper.view.draw();
        // document.getElementById("Graphs").innerHTML = "";

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
            // alert(traces.length);
            traces.forEach(function(trace){
                document.getElementById("output").innerHTML += JSON.stringify(trace) + "<br>";
                graphManager.CallFunction(trace);
            });
            document.getElementById("output").innerHTML += "Finished printing traces";
            graphManager.displayAll();
        }
    };
    xhttp.open("POST", "/trace", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(dat));
}
