#!/usr/bin/python3.5
import sys
from flask import Flask
from config import Configuration
from flask_sqlalchemy import SQLAlchemy

from flask_migrate import Migrate, MigrateCommand
from flask_script import Manager
# import value posts (object of class blueprint)
from flask_admin import Admin
# import forms for admin
from flask_admin.contrib.sqla import ModelView
from flask_security import SQLAlchemyUserDatastore
from flask_security import Security
from flask_security import current_user

from flask import redirect
from flask import url_for
from flask import request

app = Flask(__name__)
app.config.from_object(Configuration)

db = SQLAlchemy(app)

migrate = Migrate(app, db)
manager = Manager(app)
manager.add_command('db', MigrateCommand)

#ADMIN TOOLS#
from models import *

class AdminView(ModelView):
	def is_accessible(self):
		return current_user.has_role('admin')

	def inaccesible_callback(self, **kwargs):
		return redirect(url_for('security.login', next = request.url))


admin = Admin(app)
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Tag, db.session))


### Flask - security

user_datastore = SQLAlchemyUserDatastore(db, User, Role)
security = Security(app, user_datastore)