from flask import Blueprint
from flask import render_template

from models import Post, Tag
# . because this directory
from .forms import PostForm
from flask import request
from app import db

# to redirect user after creating post to main blog page
from flask import redirect
from flask import url_for

posts = Blueprint('posts', __name__, template_folder = 'templates' )

# http://localhost/blog/create
# order of location methods matters
@posts.route('/create', methods = ['POST', 'GET'])
def create_post():

	if request.method == 'POST':
		title = request.form['title']
		body = request.form['body']

		try:
			post = Post(title = title, body = body)
			db.session.add(post)
			db.session.commit()
		except:
			print("ERROR!")

		return 	redirect(url_for('posts.index'))	
	form = PostForm()
	return render_template('posts/create_post.html', form = form)



@posts.route('/<slug>/edit/', methods =['POST', 'GET'])
def edit_post(slug):
	post = Post.query.filter(Post.slug == slug).first()

	if request.method == 'POST':
		# get data from post
		form = PostForm(formdata = request.form, obj = post)
		# rewrite data in post
		form.populate_obj(post)
		# save to database
		db.session.commit()

		return redirect(utl_for('posts.post_detail', slug = post.slug))

	form = PostForm(obj = post)
	return render_template('posts/edit_post.html', post=post, form=form)


@posts.route('/')
def index():
	# when we push button search , the name of our search puts to var q.
	# request is a standart Flask method
	# q contains either name of search or ''
	q = request.args.get('q')

	page = request.args.get('page')

	if page and page.isdigit():
		page = int(page)
	else:
		page = 1

	if q:
		posts = Post.query.filter(Post.title.contains(q) | Post.body.contains(q))
	else:
		posts = Post.query.order_by(Post.created.desc())
	
	# page - number of page 
	# per_page number of pages on every page
	pages = posts.paginate(page=page, per_page=6)

	return render_template('posts/index.html', pages = pages)


# http://localhost/blog/First-post
# slug is "First-post"
# the first - post is take to function post_detail and Post.slug search in slugs first-post
# in post we have refernce to determined class object
@posts.route('/<slug>')
def post_detail(slug):
	post = Post.query.filter(Post.slug == slug).first()
	tags = post.tags
	return render_template('posts/post_detail.html', post = post, tags = tags)

# need to write tag because , may think this is not tag but post, specify /tag/
# http://localhost/blog/tag/python
# slug in tag_detail is python
@posts.route('/tag/<slug>')
def tag_detail(slug):
	tag = Tag.query.filter(Tag.slug == slug).first()
	posts = tag.posts.all()
	return render_template('posts/tag_detail.html', tag = tag, posts = posts)