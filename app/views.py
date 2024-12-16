from flask import request, render_template

def register_routes(app):
    @app.route('/')
    def main():
        return render_template("base.html", title='Main Page')

    @app.route('/resume')
    def resume():
        return render_template('resume.html', title='My resume')

    @app.route('/homepage') 
    def home():
        """View for the Home page of your website."""
        agent = request.user_agent
        return render_template("home.html", agent=agent)
