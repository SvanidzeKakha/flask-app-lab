from . import users_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta, datetime
from .forms import RegisterForm, LoginForm, UpdateAccountForm
from .models import User
from app import db, bcrypt
from flask_login import login_user, current_user, logout_user, login_required

@users_bp.route("/set_color_scheme/<scheme>")
def set_color_scheme(scheme):
    if scheme not in ['light', 'dark']:
        flash("Error: Invalid color scheme.", "danger")
    else:
        resp = make_response(redirect(url_for("users.get_profile")))
        resp.set_cookie('color_scheme', scheme, max_age=30 * 24 * 60 * 60)
        flash(f"Success: Color scheme changed to '{scheme}'.", "success")
        return resp

from flask_login import login_required, current_user

@users_bp.route("/profile", methods=['GET', 'POST'])
@login_required
def get_profile():
    username_value = current_user.username
    cookies = request.cookies
    color_scheme = cookies.get('color_scheme', 'light')

    if request.method == "POST":
        action = request.form.get("action")
        cookie_key = request.form.get("cookie_key")
        cookie_value = request.form.get("cookie_value")
        cookie_expiry = request.form.get("cookie_expiry")

        resp = make_response(redirect(url_for("users.get_profile")))

        if action == "add":
            resp.set_cookie(cookie_key, cookie_value, max_age=int(cookie_expiry))
            flash(f"Success: Cookie '{cookie_key}' added.", "success")
            return resp

        elif action == "delete":
            resp.delete_cookie(cookie_key)
            flash(f"Success: Cookie '{cookie_key}' deleted.", "success")
            return resp

    return render_template("profile.html", username=username_value, cookies=cookies, color_scheme=color_scheme)
@users_bp.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = UpdateAccountForm()

    # Populate the form with current user's data
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me
    
    if form.validate_on_submit():
        # Update the user's profile
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        
        # If password is provided, update it as well
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password
        
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    
    return render_template('edit_profile.html', form=form)
@users_bp.route('/account', methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()

    if form.validate_on_submit():
        # Update the user's profile details
        current_user.username = form.username.data
        current_user.email = form.email.data
        current_user.about_me = form.about_me.data
        current_user.last_seen = datetime.utcnow()

        # Update password if provided
        if form.password.data:
            hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
            current_user.password = hashed_password

        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))

    elif request.method == 'GET':
        # Pre-populate the form with current user's details
        form.username.data = current_user.username
        form.email.data = current_user.email
        form.about_me.data = current_user.about_me

    return render_template('account.html', title='Account', form=form)


@users_bp.route('/all_users')
@login_required
def all_users():
    # Fetch all users from the database
    users = User.query.all()
    
    # Count the number of users
    user_count = len(users)
    
    return render_template('all_users.html', users=users, user_count=user_count)

@users_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
    
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(
            username=form.username.data,
            email=form.email.data,
            password=hashed_password
        )
        try:
            db.session.add(user)
            db.session.commit()
            
            login_user(user)
            flash(f'Account created for {form.username.data}!', 'success')
            return redirect(url_for('users.account'))
        except Exception as e:
            db.session.rollback()
            flash('Error creating the account. Please try again.', 'danger')
            print(f"Error: {e}")
    
    return render_template('register.html', form=form, title='Register')

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('users.account'))
   
    form = LoginForm()
    print("Form data:", request.form)
    print("Form validate_on_submit:", form.validate_on_submit())
    
    if form.validate_on_submit():
        print("Form validated successfully")
        user = User.query.filter_by(email=form.email.data).first()
        
        if user:
            print(f"User found: {user.email}")
            if user.check_pass(form.password.data):
                login_user(user)
                session['username'] = user.username
                flash('Login successful', 'success')
                return redirect(url_for('users.account'))
            else:
                print("Password check failed")
                flash('Invalid email or password', 'danger')
        else:
            print("No user found with this email")
            flash('Invalid email or password', 'danger')
    
    if form.errors:
        print("Form validation errors:")
        for field, errors in form.errors.items():
            print(f"{field}: {errors}")
    
    return render_template("login.html", form=form)

@users_bp.route("/logout")
def logout():
    logout_user()
    session.pop('username', None)
    flash('You have been logged out', 'info')
    return redirect(url_for("users.get_profile"))

@users_bp.route("/hi/<string:name>")
def greetings(name):
    name = name.upper()
    age = request.args.get("age", None, int)   

    return render_template("hi.html", name=name, age=age)

@users_bp.route("/admin")
def admin():
    to_url = url_for("users.greetings", name="administrator", age=45, _external=True)
    print(to_url)
    return redirect(to_url)

@users_bp.route('/set_cookie')
def set_cookie():
    response = make_response('Кука встановлена')
    response.set_cookie('username', 'student', expires=datetime.now()+timedelta(seconds=60))
    response.set_cookie('colour', 'black', max_age=timedelta(seconds=60))
    return response

@users_bp.route('/get_cookie')
def get_cookie():
    username = request.cookies.get('username')
    return f'Користувач: {username}'

@users_bp.route('/delete_cookie')
def delete_cookie():
    response = make_response('Кука видалена')
    response.set_cookie('username', '', expires=0) # response.set_cookie('username', '', max_age=0)
    return response