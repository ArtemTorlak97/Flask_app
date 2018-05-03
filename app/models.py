from app import db
from datetime import datetime
import re

def slugify(s):
	pattern = r'[^\w+]'
	return re.sub(pattern, '-', s)

#db is a sqlalchemy object. And it has a special data type: Table
#post_tags - is a name
#When we have created a table we need to point relation between tables
post_tags = db.Table('post_tags',
						db.Column('post_id', db.Integer, db.ForeignKey('post.id')),
						db.Column('tag_id', db.Integer, db.ForeignKey('tag.id'))
	)


#need to create new property in Post
class Post(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	title = db.Column(db.String(140))
	#slug - URL
	slug = db.Column(db.String(140), unique = True)
	body = db.Column(db.Text)
	created = db.Column(db.DateTime, default = datetime.now())

#*args - list, all we put to artgs will be stored in list
##**kwargs - key, word (will be stored in dictionary)
	def __init__(self, *args, **kwargs):
		#to take constructor of base class
		super(Post, self).__init__(*args, **kwargs)
		self.generate_slug()

#backref - references from tags to post and reversed
#lazy
	tags = db.relationship('Tag', secondary = post_tags, backref = db.backref('posts', lazy = 'dynamic'))

	def generate_slug(self):
		if self.title:
			self.slug = slugify(self.title)

	def __repr__(self):
		#turn id to {} and title to {}
		return '<Post id: {}, title: {}>'.format(self.id, self.title)

class Tag(db.Model):
	id = db.Column(db.Integer, primary_key = True)
	name = db.Column(db.String(100))
	slug = db.Column(db.String(100))

	def __init__(self, *args, **kwargs):
		super(Tag, self).__init__(*args, **kwargs)
		self.slug = slugify(self.name)

	def __repr__(self):
		return '<Tag id: {}, name: {}>'. format(self.id, self.name)