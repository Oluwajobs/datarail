# importing dependencies
import os
import secrets
from PIL import Image  # used for resizing images
from flask import redirect, render_template, flash, url_for, request, abort
from sqlalchemy import desc
from datarail.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm, RequestResetForm, ResetPasswordForm
from datarail.models import Post, User
from datarail import app, bcrypt, db, mail
from flask_login import login_required, login_user, logout_user, current_user
from flask_mail import Message


#--------------------------------------------------#
# Routes
#--------------------------------------------------#


# route for home page
@app.route("/")
@app.route("/home")
def home():
    page = request.args.get("page", 1, type=int)
    # limiting the number of items on a page using pagination
    # using order_by desc to output posts based on the latest
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(page=page, per_page=5)  
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
    random_hex = secrets.token_hex(8)  # generates a random hex token of 8 byte 
    _, fext = os.path.splitext(form_picture.filename)  # splits the file name from the extention
    picture_new_name = random_hex + fext  # concat of the random number and the image extension
    picture_path = os.path.join(
        app.root_path, "static/profile_pics", picture_new_name)
    # saving the user uploaded picture to the path we created

    # resizing the image using Pillow
    output_size = (150, 150)
    i = Image.open(form_picture)  # parsing the form.picture.data input into Pillow
    i.thumbnail(output_size)  # resizing to specified dim
    i.save(picture_path)  # saving picture to path with our new size and random hex name

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

#-------------------------------------------#
# Route for Creating Posts      
#-------------------------------------------#

@app.route('/post/new', methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    
    if form.validate_on_submit():
        # passing form data into our Post table
        title = form.title.data
        content = form.content.data
        post = Post(title=title, content=content, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash("Your post has been created", "success")
        return redirect(url_for('home'))
    return render_template('create_post.html', title="New Post", legend="New Post", form=form)


#-------------------------------------------#
# Route for getting each Posts
#-------------------------------------------#
@app.route('/post/<int:post_id>', methods=['GET'])
@login_required
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', post=post, title=post.title)



#-------------------------------------------#
# Route for Updating Posts      
#-------------------------------------------#


@app.route('/post/<int:post_id>/edit', methods=['GET', 'POST'])
@login_required
def edit_post(post_id):
    # get the post to be edited first
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data  # they are already in the database we are just updating them.
        post.content = form.content.data
        
        db.session.commit()
        flash("Your post has been updated", "success")
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title="Edit Post", legend="Edit Post", form=form)

    
#-------------------------------------------#
# Route for Deleting each Posts
#-------------------------------------------#
@app.route('/post/<int:post_id>/delete', methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()  # Always commit after making changes to the db for it to persist.
    flash("Your post has been deleted", "success")
    return redirect(url_for('home'))


@app.route("/user/<string:username>")
def user_post(username):
    page = request.args.get("page", 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()  # Getting the username of the post
    posts = Post.query.filter_by(author=user).order_by(
        Post.date_posted.desc()).paginate(page=page, per_page=5)
    return render_template('user_post.html', posts=posts, user=user)

#-----------------------------------#
# creating a fuction to send email with token to user
#-----------------------------------#
def send_reset_email(user):
    token = user.get_reset_token()
    msg = Message(subject="Password Reset Request", recipients=[user.email], sender="noreply@datarail.com")
    msg.body = f'''To reset your password, visit the following link:
{url_for('reset_token', token=token, _external=True)}
If you did not make this request, simply ignore this email and no changes will be made to your account
'''
# the _external allows the app to generate an absolute path for our url
    mail.send(msg)  # sends the email to our user

#-----------------------------------#
# creating a route for password reset request
#-----------------------------------#
@app.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    # make sure user is logged out before they can reset password
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash("An email has been sent with instructions to reset your password. Make sure to check your inbox or spam", "info")
        return redirect(url_for('login'))
    return render_template('reset_request.html', title="Reset Password", form=form)


#-----------------------------------#
# creating a route for password reset
#-----------------------------------#
@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    # make sure user is logged out before they can reset password
    if current_user.is_authenticated:
        return redirect(url_for('home'))
    # validate token provided by user
    user = User.verify_reset_token(token)
    if not user:
        flash('Token is invalid or expired', 'warning')
        return redirect(url_for('reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        password = form.password.data
        # hashing the password
        hashed_password = bcrypt.generate_password_hash(
            password).decode('utf-8')
        # updating user password in our db
        user.password = hashed_password
        # commiting it into our db
        db.session.commit()
        # Directing user to login page
        flash("Your password has been successfully updated! You are now able to log in",
              category='success')
        return redirect(url_for('login'))
    return render_template('reset_token.html', title="Reset Password", form=form)