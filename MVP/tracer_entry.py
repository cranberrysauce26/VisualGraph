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
        if self.error != None:
            print("error:", self.error, end='')
        else:
            print("command_name:", self.command_name, ", args", self.args, ", return_value:", self.return_value, ", line_number:", self.line_number, ", graph_id:", self.graph_id, end='')