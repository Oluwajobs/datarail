# importing dependencies
import os
import secrets
from flask import redirect, render_template, flash, url_for, request
from datarail.forms import RegistrationForm, LoginForm, UpdateAccountForm
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


#----------------------------------------------------------------------#
# Function for renaming and resizing picture data
#----------------------------------------------------------------------#

def save_picture(form_picture):
    random_hex = secrets.token_hex(8)
    _, fext = os.path.splitext(form_picture.filename)
    picture_new_name = random_hex + fext
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_new_name)
    # saving the user uploaded picture to the path we created
    form_picture.save(picture_path)

    return picture_new_name


@app.route("/account", methods=["GET", "POST"])
@login_required
def account():
    form = UpdateAccountForm()
    image_file = url_for('static', filename=f'profile_pics/{current_user.image_file}')
    if form.validate_on_submit():
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()  # commiting the change in user information
        flash("Your account information has been updated", "success")
        return redirect(url_for('account'))

    elif request.method == "GET":
        form.username.data = current_user.username
        form.email.data = current_user.email
    return render_template('account.html', title='Account', image_file=image_file, form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('login'))
