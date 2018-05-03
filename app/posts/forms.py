from wtforms import Form, StringField, TextAreaField
#wtFrorms - an agreement between forms 

#mininaml fields : Title and Body
class PostForm(Form):
	title = StringField('Title')
	body = TextAreaField('Body')
	
