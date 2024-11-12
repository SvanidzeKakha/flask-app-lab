from . import post_bp
import json
from .forms import PostForm
from flask import render_template, abort, flash, redirect, url_for

posts = [
    {"id": 1, 'title': 'My First Post', 'content': 'This is the content of my first post.', 'author': 'John Doe'},
    {"id": 2, 'title': 'Another Day', 'content': 'Today I learned about Flask macros.', 'author': 'Jane Smith'},
    {"id": 3, 'title': 'Flask and Jinja2', 'content': 'Jinja2 is powerful for templating.', 'author': 'Mike Lee'}
] 

@post_bp.route('/') 
def get_posts():
    try:
        with open('app/posts/templates/posts/posts.json', 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []
    return render_template("posts/posts.html", posts=posts)

@post_bp.route('/<int:id>') 
def detail_post(id):
    try:
        with open('app/posts/templates/posts/posts.json', 'r') as f:
            posts = json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        posts = []

    post = next((post for post in posts if post["id"] == id), None)
    if post is None:
        abort(404)
        
    return render_template("posts/detail_post.html", post=post)

@post_bp.route('/add_post', methods = ['GET', 'POST'])
def add_post():
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        content = form.content.data

        try:
            with open('app/posts/templates/posts/posts.json', 'r') as f:
                posts = json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            posts = []

        next_id = max([post["id"] for post in posts], default=0) + 1
        post = {"id": next_id, "title": title, "content": content, "author": "Anonymous"}

        posts.append(post)

        with open('app/posts/templates/posts/posts.json', 'w') as f:
            json.dump(posts, f, indent=4)

        flash('Post added successfully', 'success')
        return redirect(url_for('post.get_posts'))

    return render_template('posts/add_post.html', form = form)

@post_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404