import os

class Configuration(object):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://artem:123@localhost/test1'
	SECRET_KEY = 'MY_SECRET'
	SECURITY_PASSWORD_SALT = 'salt'
	SECURITY_PASSWORD_HASH = 'sha512_crypt'

	SECURITY_LOGIN_URL='/login'
	SECURITY_LOGOUT_URL='/logout'
	SECURITY_LOGIN_USER_TEMPLATE = "login.html"
	SECURITY_POST_LOGIN_VIEW = "/"
	
	MAIL_SERVER = 'smtp.googlemail.com'
	MAIL_PORT = 465
	MAIL_USE_TLS = False
	MAIL_USE_SSL = True

    # gmail authentication
	#MAIL_USERNAME = os.environ['APP_MAIL_USERNAME']
	#MAIL_PASSWORD = os.environ['APP_MAIL_PASSWORD']
	MAIL_USERNAME = "unimpossible12@gmail.com"
	MAIL_PASSWORD = "077779493"

    # mail accounts
	MAIL_DEFAULT_SENDER = 'unimpossible12@gmail.com'