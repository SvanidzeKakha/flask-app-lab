from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from sqlalchemy.orm import DeclarativeBase
from flask_login import LoginManager
from flask_bcrypt import Bcrypt
from config import config
from .views import register_routes

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
migrate = Migrate()
bcrypt = Bcrypt()
login_manager = LoginManager()
login_manager.login_view = 'users.login'
login_manager.login_message = 'Please login to access this page'
login_manager.login_message_category = 'warning'

def create_app(config_name = "default"):
    app = Flask(__name__)
    app.config.from_object(config.get(config_name))
   
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)
    bcrypt.init_app(app)

    with app.app_context(): 
        from . import views

        from app.posts import post_bp
        app.register_blueprint(post_bp, url_prefix="/posts")

        from app.users import users_bp
        app.register_blueprint(users_bp, url_prefix="/users")
        
        from app.posts.models import Post
        from app.users.models import User

        register_routes(app)
        
    return app