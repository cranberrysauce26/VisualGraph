class Vertex {
    constructor(id, graph, color) {
        this.id = id;
        this.graph = graph;
        this.properties = {color: 'orange'};
    }

    setProperty(name, value){
        this.properties[name] = value;
    }
    //
    // printProperties(position) {
    //     var text = new paper.PointText(position);
    //     text.justification = "center";
    //     text.fillColor = 'black';
    //     text.fontSize = '20px';
    //     text.content = JSON.stringify(this.properties);
    // }
}
