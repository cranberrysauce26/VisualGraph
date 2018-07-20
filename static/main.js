var graphManager = new GraphManager();

function visualize() {
    console.log("Visualize called");
    var text = editor.getValue();
    var dat = { code: text }
    if (text.length == 0) {
        document.getElementById("output").innerHTML = "You didn't enter anything!";
        return;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function () {
        if (this.readyState == 4 && this.status == 200) {
            document.getElementById("output").innerHTML = "Traces:<br>";
            var str = this.responseText;
            var traces = JSON.parse(str);
            console.log(traces);
            traces.forEach(function (trace) {
                document.getElementById("output").innerHTML += JSON.stringify(trace) + "<br>";
                graphManager.callFunction(trace);
            });
            document.getElementById("output").innerHTML += "Finished printing traces";
            graphManager.displayAll();
        }
    };
    xhttp.open("POST", "/trace", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(dat));
}
