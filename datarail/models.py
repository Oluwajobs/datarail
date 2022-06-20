# importing dependencies
from tkinter.messagebox import NO
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer   # package for generating token
from datetime import datetime
from datarail import db, login_manager, app
from flask_login import UserMixin


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

    def get_reset_token(self, expire_sec=1800):
        """This method creates a payload using the user_id and token generated from itsdangerous"""
        s = Serializer(app.config['SECRET_KEY'], expire_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')

    @staticmethod
    def verify_reset_token(token):
        """This method verifies if the user has a valid token to reset their password"""
        s = Serializer(app.config['SECRET_KEY'])
        try:
            user_id = s.loads(token)['user_id']  # returns a tuple of our payload...i.e. user_id and header
        except:
            return None
        return User.query.get(user_id)

    def __repr__(self):
        return f"({self.username}, {self.email}, {self.image_file})"

# Table for user posts


class Post(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False,
                            default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # grabs the author of each post form the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"({self.title}, {self.date_posted})"
