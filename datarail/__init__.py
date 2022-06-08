# importing dependencies
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # import database dependency
from flask_bcrypt import Bcrypt  # import module for hashing password
from flask_login import LoginManager  # import module for handling user sessions


app = Flask(__name__)  # creating the flask application
app.config['SECRET_KEY'] = "395e5168605a9fdd39af680175df2805"
# creating an sqlite database in our relative path
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)  # initializing app
bcrypt = Bcrypt(app)  # initializing app
login_manager = LoginManager(app)  #initializing our LoginManage to handle user sessions
login_manager.login_view = 'login'  # telling login_manager what route to direct unauthorized users to
login_manager.login_message_category = 'info'  #b Bootstrap category for our message to user

from datarail import routes  # importing the routes