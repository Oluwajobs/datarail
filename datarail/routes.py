# importing dependencies
from flask import redirect, render_template, flash, url_for
from flask_sqlalchemy import SQLAlchemy  # import database dependency
from datarail.forms import RegistrationForm, LoginForm
from datarail.models import posts
from datarail import app


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
        # returning a message fpr user and giving it a success category
        flash(
            f"Account successfully created for {form.username.data}!", category='success')
        return redirect(url_for('home'))

    return render_template('register.html', title='Register', form=form)

# route for login page


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@datarail.com' and form.password.data == 'testing':
            flash("You have been successfully logged in!", "success")
            return redirect(url_for('home'))
        else:
            flash(
                "Login was unsuccessful. Check your information and try again", "danger")
    return render_template('login.html', title='Login', form=form)
