from flask import Flask, request, render_template
from MVP.tracer import get_trace_as_json

app = Flask(__name__)

app.debug = True

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/trace', methods=['POST'])
def trace():
	data = request.get_json()
	return get_trace_as_json(data['code'], __builtins__)

# https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
if __name__ == '__main__':
	app.run()
