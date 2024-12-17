from app import db, login_manager, bcrypt
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def user_loader(user_id):
    return User.query.get(int(user_id))

def hash_pass(password):
    return bcrypt.generate_password_hash(password).decode('utf-8')

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=True, default='default.jpg')
    about_me = db.Column(db.Text, nullable=True)
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)
    password = db.Column(db.String(60), nullable=False)
   
    def get_id(self):
        return str(self.id)
    
    def __repr__(self):
        return f"User('{self.email}')"
    
    def check_pass(self, password):
        return bcrypt.check_password_hash(self.password, password)