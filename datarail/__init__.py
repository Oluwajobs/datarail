# importing dependencies
import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy  # import database dependency
from flask_bcrypt import Bcrypt  # import module for hashing password
from flask_login import LoginManager  # import module for handling user sessions
from flask_mail import Mail


app = Flask(__name__)  # creating the flask application
app.config['SECRET_KEY'] = "395e5168605a9fdd39af680175df2805"
# creating an sqlite database in our relative path
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"
db = SQLAlchemy(app)  # initializing app
bcrypt = Bcrypt(app)  # initializing app
login_manager = LoginManager(app)  #initializing our LoginManage to handle user sessions
login_manager.login_view = 'login'  # telling login_manager what route to direct unauthorized users to
login_manager.login_message_category = 'info'  #b Bootstrap category for our message to user
#------Set up Gmail SMTP SERVER--------------#
# app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_SERVER'] = 'smtp.gmail.com'
# app.config['MAIL_PORT'] = 587
app.config['MAIL_PORT'] = 465
# app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True
app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')

#----------End-------------------------------#
mail = Mail(app)
from datarail import routes  # importing the routes