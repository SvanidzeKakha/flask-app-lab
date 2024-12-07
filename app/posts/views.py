from . import post_bp
from .forms import PostForm
from flask import render_template, abort, flash, redirect, url_for
from .models import Post
from .models import Tag
from app.users.models import User
from app import db

@post_bp.route('/')
def get_posts():
    posts = Post.query.order_by(Post.date_posted.desc()).all()  # Querying the database and sorting by date_posted in descending order
    return render_template("posts/posts.html", posts=posts)

@post_bp.route('/<int:id>')  # The route will accept an 'id' parameter in the URL
def detail_post(id):
    post = Post.query.get_or_404(id)  # Query the database for the post by its ID; returns 404 if not found
    return render_template("posts/detail_post.html", post=post)

@post_bp.route('/add_post', methods=['GET', 'POST'])
def add_post():
    form = PostForm()

    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    tags = Tag.query.all()
    form.tags_id.choices = [(tag.id, tag.name) for tag in tags]

    if form.validate_on_submit():
        post = Post(
            title=form.title.data,
            content=form.content.data,
            category=form.category.data,
            is_active=form.is_active.data,
            date_posted=form.date_posted.data,
        )
        try:
            db.session.add(post)
            db.session.commit()
            flash('Post added successfully!', 'success')
            return redirect(url_for('post.get_posts'))
        except Exception as e:
            db.session.rollback()
            flash('Error adding the post. Please try again.', 'danger')
            print(f"Error: {e}")

    return render_template('posts/add_post.html', form=form)

@post_bp.route('/delete/<int:id>', methods=['POST'])
def delete_post(id):
    post = Post.query.get_or_404(id)  # Fetch the post from the database
    try:
        db.session.delete(post)  # Delete the post from the session
        db.session.commit()  # Commit the changes to the database
        flash('Post deleted successfully!', 'success')  # Flash a success message
    except Exception as e:
        db.session.rollback()  # If an error occurs, rollback the transaction
        flash('Error deleting the post. Please try again.', 'danger')
        print(f"Error: {e}")
    
    return redirect(url_for('post.get_posts'))  # Redirect back to the posts list page

@post_bp.route('/edit/<int:id>', methods=['GET', 'POST'])
def edit_post(id):
    post = db.get_or_404(Post, id)
    form = PostForm(obj=post)

    # Populate choices for author and tags
    authors = User.query.all()
    form.author_id.choices = [(author.id, author.username) for author in authors]
    tags = Tag.query.all()
    form.tags_id.choices = [(tag.id, tag.name) for tag in tags]

    # Pre-fill tag selection with existing tags for this post
    form.tags_id.data = [tag.id for tag in post.tags]

    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        post.category = form.category.data
        post.is_active = form.is_active.data
        post.date_posted = form.date_posted.data
        post.user_id = form.author_id.data

        # Update tags
        selected_tags = Tag.query.filter(Tag.id.in_(form.tags_id.data)).all()
        post.tags = selected_tags

        try:
            db.session.commit()
            flash('Post updated successfully!', 'success')
            return redirect(url_for('post.get_posts'))
        except Exception as e:
            db.session.rollback()
            flash('Error updating the post. Please try again.', 'danger')
            print(f"Error: {e}")

    return render_template('posts/add_post.html', form=form)

@post_bp.errorhandler(404)
def page_not_found(error):
    return render_template('404.html'), 404