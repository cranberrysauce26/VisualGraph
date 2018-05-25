import json

class TraceEntry:
    def __init__(self, command_name=None, graph_type=None, graph_id=None, args=[], return_value=None, line_number=None, error=None):
        self.command_name = command_name
        self.graph_type = graph_type
        self.graph_id = graph_id
        self.args = args
        self.return_value = return_value
        self.line_number = line_number
        self.error = error

    # for convenience
    def display(self):
        # print(self._trace_values)
        if self.error != None:
            print("error:", self.error, end='')
        else:
            print("command_name:", self.command_name, ", args", self.args, ", return_value:", self.return_value, ", line_number:", self.line_number, ", graph_id:", self.graph_id, end='')

class TraceEntryJSONEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, TraceEntry):
            return {
                "command_name": obj.command_name,
                "graph_type": obj.graph_type,
                "graph_id": obj.graph_id,
                "args": obj.args,
                "return_value": obj.return_value,
                "line_number": obj.line_number,
                "error": obj.error
            }
        return json.JSONEncoder.default(self, obj)

def add_trace_entry(command_name, graph_type, graph_id, args=[], return_value=None, line_number=None, error=None):
    return TraceEntry(command_name, graph_type, graph_id, args, return_value, line_number, error)

if __name__ == '__main__':
    trace_entry = TraceEntry()
    trace_entry.error = "I am an error"
    trace_entry_arr = [TraceEntry(), TraceEntry()]
    # do it like this
    print(json.dumps(trace_entry, cls=TraceEntryJSONEncoder))
    # or like this
    print(TraceEntryJSONEncoder().encode(trace_entry_arr))