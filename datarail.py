# importing dependencies
from datetime import datetime
from flask import Flask, redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy  # import database dependency
from forms import RegistrationForm, LoginForm

app = Flask(__name__)  # creating the flask application
app.config['SECRET_KEY'] = "395e5168605a9fdd39af680175df2805"
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///site.db"  # creating an sqlite database in our relative path
db = SQLAlchemy(app)


# Creating a dummy database query
posts = [
    {'author': 'John Doe', 
    'title': 'Blog Post 1', 
    'content': 'This is my first blog post',
    'date_posted': 'June 2, 2022'},

    {'author': 'Sarah Lee',
     'title': 'Blog Post 1',
     'content': 'This is my second blog post',
     'date_posted': 'June 2, 2022'}]

#--------------------------------------------------#
# Models
# Creating Our Model using classes that inherit from db.Model
#--------------------------------------------------#
# User table
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    email = db.Column(db.String(50), nullable=False, unique=True)
    image_file = db.Column(db.String(120), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    # establishing one to many relationship with the post table
    post = db.relationship('Post', backref='author', lazy=True)

    def __repr__(self):
        return f"({self.username}, {self.email}, {self.image_file})"

# Table for user posts
class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(60), nullable=False, unique=True)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    # grbas the author of each post form the user table
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    
    def __repr__(self):
        return f"({self.title}, {self.date_posted})"



#--------------------------------------------------#
# Routes
#--------------------------------------------------#


# route for home page
@app.route("/")
@app.route("/home")
def home():
    return render_template('home.html', posts=posts)

# route for about page
@app.route("/about")
def about():
    title = "About"
    return render_template('about.html', title=title)

# route for register page
@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f"Account successfully created for {form.username.data}!", category='success')  # returning a message fpr user and giving it a success category
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

# route for login page
@app.route("/login", methods=["POST", "GET"])
def login():
    form=LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@datarail.com' and form.password.data == 'testing':
            flash("You have been successfully logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash("Login was unsuccessful. Check your information and try again", "danger")
    return render_template('login.html', title='Login', form=form)



# making sure we can run our app as a python script
if __name__ == "__main__":
    app.run(debug=True)