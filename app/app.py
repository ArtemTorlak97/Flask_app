#!/usr/bin/python3.5
import sys
from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# import value posts (object of class blueprint)
from flask_admin import Admin
from flask_admin import AdminIndexView
# import forms for admin
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user

from flask import redirect
from flask import url_for
from flask import request
from flask import render_template
from flask import session
from flask import flash

from generate_token import generate_confirmation_token, confirm_token
from flask_security import login_required
from flask_login import LoginManager, current_user, login_user
#from flask.ext.security.forms import LoginForm
from forms import LoginForm
from flask_mail import Message, Mail
from my_email import send_email

app = Flask(__name__)
app.config.from_object(Configuration)
mail = Mail(app)

login = LoginManager(app)

def send_email(to, subject, template):
    
    msg = Message(
        subject,
        recipients=[to],
        html=template,
        sender="from@example.com"
    )
    mail.send(msg)


db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#ADMIN TOOLS#
from models import *

class AdminMixin:
	def is_accessible(self):
		return current_user.has_role('admin')

	def inaccesible_callback(self, name, **kwargs):
		return redirect(url_for('security.login', next = request.url))

# when we change our post slug will generate automatically
class BaseModelView(ModelView):
	def on_model_change(self, form, model, is_created):
		model.generate_slug()
		return super(BaseModelView, self).on_model_change(form, model, is_created)


class AdminView(AdminMixin, ModelView):
	pass

class HomeAdminView(AdminIndexView):
	pass

class PostAdminView(AdminMixin, BaseModelView):
	form_columns = ['title', 'body', 'tags']

class TagAdminView(AdminMixin, BaseModelView):
	form_columns = ['name', 'posts']

admin = Admin(app, 'FlaskApp', url ='/', index_view = HomeAdminView(name = 'Home'))
admin.add_view(PostAdminView(Post, db.session))
admin.add_view(TagAdminView(Tag, db.session))

### Flask - security


user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)

### User registration
@app.route('/register', methods =['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    user = User(request.form['email'] , request.form['password'])
    role = Role.query.filter(Role.name == 'user')
    role = role.first()
    user_datastore.add_role_to_user(user,role)

    db.session.add(user)
    db.session.commit()

    token = generate_confirmation_token(user.email)
    confirm_url = url_for('confirm_email', token = token, _external = True)
    html = render_template('act.html', confirm_url=confirm_url)
    subject = "Please confirm your email"
    send_email(request.form['email'], subject, html)
    #login_user(user)
    flash('A confirmation email has been sent via email.', 'success')
    confirm_email(token)
    return redirect(url_for('unconfirmed'))

@app.route('/confirm/<token>')
@login_required
def confirm_email(token):
    try:
        email = confirm_token(token)
        print(email)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    user = User.query.filter_by(email=email).first_or_404()
    if user.confirmed:
        flash('Account already confirmed. Please login.', 'success')
    else:
        user.confirmed = True
        db.session.add(user)
        db.session.commit()
        flash('You have confirmed your account. Thanks!', 'success')
    return redirect(url_for('index'))

@app.route('/unconfirmed')
def unconfirmed():
    flash('Please confirm your account!', 'warning')
    return render_template('unconf.html')

