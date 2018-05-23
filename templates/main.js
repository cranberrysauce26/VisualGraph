var graphManager = new GraphManager();

function Visualize() {
    alert("Visualize Called");
    var text = $("#textbox").val();
    var dat = {code : text}
    if (text.length == 0) {
        document.getElementById("output").innerHTML = "You didn't enter anything!";
        return;
    }
    var xhttp = new XMLHttpRequest();
    xhttp.onreadystatechange = function() {
        if (this.readyState == 4 && this.status == 200) {
            alert("Outputting");
            document.getElementById("output").innerHTML = "Traces:<br>";
            var str = this.responseText;
            var traces = JSON.parse(str);
            traces.forEach(function(trace){
                // document.getElementById("output").innerHTML += "Hi "+JSON.stringify(trace) + "<br>";
                // graphManager.CallFunction(trace);
            });
        }
    };
    xhttp.open("POST", "/trace", true);
    xhttp.setRequestHeader("Content-Type", "application/json");
    xhttp.send(JSON.stringify(dat));
}
