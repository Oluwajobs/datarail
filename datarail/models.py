# importing dependencies
from datetime import datetime
from datarail import db, login_manager
from flask_login import UserMixin


# dummy data
posts = [
    {'author':'John Doe', 
    'date_posted': 'June 5, 2022', 
    'content': 'This is my first post',
    'title':'My First post!'},

    {'author':'Sarah Sun', 
    'date_posted': 'June 4, 2022', 
    'content': 'This Sarah\'s Second post',
    'title':'My Second post!'}, 
    ]

# load users
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


#--------------------------------------------------#
# Models
# Creating Our Model using classes that inherit from db.Model
#--------------------------------------------------#
# User table


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    image_file = db.Column(
        db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # establishing one to many relationship with the post table
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"({self.username}, {self.email}, {self.image_file})"

# Table for user posts


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # grbas the author of each post form the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"({self.title}, {self.date_posted})"
