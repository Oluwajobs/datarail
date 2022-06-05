# importing dependencies
from flask import Flask, redirect, render_template, flash, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)  # creating the flask application

app.config['SECRET_KEY'] = "395e5168605a9fdd39af680175df2805"

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