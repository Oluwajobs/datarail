# importing dependencies
import email
from flask import redirect, render_template, flash, url_for, request
from datarail.forms import RegistrationForm, LoginForm
from datarail.models import User, posts
from datarail import app, bcrypt, db
from flask_login import login_required, login_user, logout_user, current_user


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
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        password = form.password.data
        username = form.username.data
        email = form.email.data
        # hashing the password
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        # creating a user in our db
        user = User(username=username, email=email, password=hashed_password)
        # commiting it into our db
        db.session.add(user)
        db.session.commit()
        # Directing user to login page
        flash("Your Account has been successfully created! You are now able to log in", category='success')
        return redirect(url_for('login'))

    return render_template('register.html', title='Register', form=form)

# route for login page


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if current_user.is_authenticated:
        return redirect(url_for('home'))

    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            next_page = request.args.get('next')
            return redirect(next_page) if next_page else redirect(url_for('home'))
        else:
            flash("Login was unsuccessful. Check your information and try again", "danger")
    return render_template('login.html', title='Login', form=form)


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
