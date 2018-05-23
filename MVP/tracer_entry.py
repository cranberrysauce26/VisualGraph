import json

class TraceEntry:
    def __init__(self):
        self.error = None
        self.command_name = None
        self.args = []
        self.graph_id = None
        self.return_value = None
        self.line_number = None

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
                "error": obj.error,
                "command_name": obj.command_name,
                "args": obj.args,
                "graph_id": obj.graph_id,
                "return_value": obj.return_value,
                "line_number": obj.line_number
            }
        return json.JSONEncoder.default(self, obj)

if __name__ == '__main__':
    trace_entry = TraceEntry()
    trace_entry.error = "I am an error"
    trace_entry_arr = [TraceEntry(), TraceEntry()]
    # do it like this
    print(json.dumps(trace_entry, cls=TraceEntryJSONEncoder))
    # or like this
    print(TraceEntryJSONEncoder().encode(trace_entry_arr))