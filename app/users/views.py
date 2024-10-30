from . import users_bp
from flask import render_template, request, redirect, url_for, make_response, session, flash
from datetime import timedelta, datetime

@users_bp.route("/profile")
def get_profile():
    if "username" in session:
        username_value = session["username"]
        flash("Invalid: Every field is required.", "danger")
        return render_template("profile.html", username = username_value)
    return redirect(url_for("users.login"))

@users_bp.route("/login", methods=['GET','POST'])
def login():
    if request.method == "POST":
        username = request.form[login]
        session["username"] = username
        flash("Success: Info added successfully.", "success")
        return redirect(url_for("users.get_profile"))
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