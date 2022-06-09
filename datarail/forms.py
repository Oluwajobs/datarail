# Installing flask package for forms
from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField, EmailField, BooleanField, PasswordField, SubmitField, TextAreaField  # importing our form fields from wtforms
from wtforms.validators import DataRequired, EqualTo, Length, Email, ValidationError
from datarail.models import User
from flask_login import current_user

# creating our registration form
class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Sign Up')

    def validate_username(self, username):
        """
        Validates that the username a user is attempting to register with does not already EXIST IN THE DATABASE
        """
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError("The username is already taken. Please choose a different username.")
    
    def validate_email(self, email):
        """
        Validates that the email a user is attempting to register with does not already EXIST IN THE DATABASE
        """
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError("The email is already taken. Please choose a different email.")


# creating our login form
class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remember Me')
    submit = SubmitField('Log In')

# creating our account update form
class UpdateAccountForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    picture = FileField("Upload Profile Picture", validators=[FileAllowed(
        ['png', 'jpg'], "Images only!")])  # form field for file upload
    submit = SubmitField('Update')

    def validate_username(self, username):
        """
        Validates that the username a user is attempting to register with does not already EXIST IN THE DATABASE
        """
        if username.data != current_user.username:
            user = User.query.filter_by(username=username.data).first()
            if user:
                raise ValidationError("The username is already taken. Please choose a different username.")
    
    def validate_email(self, email):
        """
        Validates that the email a user is attempting to register with does not already EXIST IN THE DATABASE
        """
        if email.data != current_user.email:
            user = User.query.filter_by(email=email.data).first()
            if user:
                raise ValidationError("The email is already taken. Please choose a different email.")


# creating our login form
class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Post')
