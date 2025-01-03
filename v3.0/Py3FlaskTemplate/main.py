from flask import Flask
from flask import render_template
from flask import request

from flask_wtf import FlaskForm

from wtforms import StringField, SubmitField

app = Flask(__name__)

@app.route('/')
def serve_index():
	return render_template('framework.html'), 200;

@app.route('/', defaults={'path1': '', 'path2': ''})
@app.route('/<path:path1>', defaults={'path2': ''})
@app.route('/<path:path1>/<path:path2>')
def default_route(path1, path2):
	return render_template('forbidden.html'), 404;

@app.errorhandler(Exception)
def all_errors(e):
	return default_route();

if __name__ == '__main__':
	print("Staring flask server from main.py."); #!Debugging
	app.run(debug=True)
