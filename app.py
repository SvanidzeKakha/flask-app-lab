from flask import Flask, request, redirect, url_for, render_template, abort

app = Flask(__name__)
app.config.from_pyfile("config.py")

@app.route('/')
def main():
    return render_template("base.html")

@app.route('/resume')
def resume():
    return render_template('resume.html', title='My resume')

if __name__ == "__main__":
    app.run()