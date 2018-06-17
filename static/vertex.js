class Vertex {
    constructor(id, graph, color) {
        this.id = id;
        this.graph = graph;
        this.properties = {color: 'orange'};
    }

    setProperty(name, value){
        this.properties[name] = value;
    }
}
