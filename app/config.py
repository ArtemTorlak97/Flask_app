class Configuration(object):
	DEBUG = True
	SQLALCHEMY_TRACK_MODIFICATIONS = False
	SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://artem:123@localhost/test1'
	SECRET_KEY = 'MY_SECRET'

	### Flask-sqcurity
	### ?????????
	### artem@test.ru
	### admin
	SECURITY_PASSWORD_SALT = 'salt'
	SECURITY_PASSWORD_HASH = 'sha512_crypt'