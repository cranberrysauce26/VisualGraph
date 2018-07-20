class Vertex {
    constructor(id, graph) {
        this.id = id;
        this.graph = graph; // is this necessary?
        this.properties = { color: 'orange' }; // default vertex color
    }

    // copy constructor
    copy() {
        var v = new Vertex(this.id, this.graph);
        for (var property in this.properties){
            v.properties[property] = this.properties[property];
        }
        return v;
    }

    setProperty(name, value) {
        this.properties[name] = value;
    }
}
