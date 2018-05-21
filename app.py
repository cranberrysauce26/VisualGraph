from flask import Flask, request
from MVP.tracer import Tracer

app = Flask(__name__)

app.debug = True

@app.route('/')
def index():
	return 'INDEX'

@app.route('/trace')
def trace():
	code = request.args.get('code')
	if code == None:
		return 'Not found'
	tracer=Tracer()
	tracer.execute(code, __builtins__)
	trace = tracer.trace
	for i, trace_entry in enumerate(trace):
		print('trace[{0}]: '.format(i), end='')
		trace_entry.display()
		print(' ')
	return code

# https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
if __name__ == '__main__':
	app.run()
