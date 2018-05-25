from flask import render_template
from flask import Blueprint

from .models import post

posts = Blueprint('posts', __name__, template_folder='templates')

@posts.route('/')
def index():
	posts = post.query.all()

	return render_template('posts/index.html', posts=posts)


@posts.route('/<slug>')
def post_detail(slug):
	posts = post.query.filter(post.slug==slug).first()

	return render_template('posts/post_detail.html', post=posts)