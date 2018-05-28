from flask import Flask, request, render_template
from visugraph.trace import get_trace

app = Flask(__name__)

app.debug = True

@app.route('/')
def index():
	return render_template('index.html')

@app.route('/trace', methods=['POST'])
def trace():
	data = request.get_json()
	return get_trace(data)

@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404

# https://chrisyeh96.github.io/2017/08/08/definitive-guide-python-imports.html
if __name__ == '__main__':
	app.run()
