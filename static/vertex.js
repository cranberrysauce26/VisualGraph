class Vertex {
    constructor(id, graph, color) {
        this.id = id;
        this.graph = graph; // is this necessary?
        this.properties = { color: 'orange' };
    }

    // copy constructor
    constructor(v) {
        this.id = v.id;
        this.graph = v.graph;
        this.color = v.color;
    }

    setProperty(name, value) {
        this.properties[name] = value;
    }
}
