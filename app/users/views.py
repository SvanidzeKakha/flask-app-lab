from . import users_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta, datetime

@users_bp.route("/set_color_scheme/<scheme>")
def set_color_scheme(scheme):
    if scheme not in ['light', 'dark']:
        flash("Error: Invalid color scheme.", "danger")
    else:
        resp = make_response(redirect(url_for("users.get_profile")))
        resp.set_cookie('color_scheme', scheme, max_age=30 * 24 * 60 * 60)
        flash(f"Success: Color scheme changed to '{scheme}'.", "success")
        return resp

@users_bp.route("/profile", methods=['GET', 'POST'])
def get_profile():
    if "username" not in session:
        flash("Error: You must be logged in to access this page.", "danger")
        return redirect(url_for("users.login"))

    username_value = session["username"]
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

@users_bp.route("/login", methods=['GET', 'POST'])
def login():
    correct_username = "User1"
    correct_password = "password123"

    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        if username == correct_username and password == correct_password:
            session["username"] = username
            flash("Success: Logged in successfully.", "success")
            return redirect(url_for("users.get_profile"))
        else:
            flash("Error: Invalid username or password.", "danger")
            return redirect(url_for("users.login"))

    return render_template("login.html")

@users_bp.route("/logout")
def logout():
    session.pop('username', None)
    session.pop('age', None)
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