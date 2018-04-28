from app import app
from flask import render_template

#@ - means decorator
@app.route('/')
def index():
	return render_template('index.html') 	