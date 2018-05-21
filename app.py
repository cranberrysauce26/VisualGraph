# from flask import Flask, render_template

# app = Flask(__name__)

# app.debug = True

# @app.route('/')
# def index():
# 	return 'INDEX'

# if __name__ == '__main__':
# 	app.run()

class CustomError(Exception):
	def __init__(self, msg):
		pass


def div(a, b):
	try:
		return a/b
	except Exception as e:
		print("error: {0}".format(e))

div(10, 0)

try:
	raise Exception("hey", "there")
except Exception as e:
	print("error:",e)