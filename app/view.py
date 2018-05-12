from app import app
from flask import render_template
from flask_security import login_required
from flask_mail import Message, Mail

#@ - means decorator
@app.route('/')
def index():
	return render_template('index.html') 	


