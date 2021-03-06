"""Forms for Flask Notes."""

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import InputRequired, Email, Length


class RegisterForm(FlaskForm):
    """New User Register Form."""

    username = StringField("Username",
                           validators=[InputRequired(), Length(max=20)])

    password = PasswordField("Password",
                           validators=[InputRequired()])

    email = StringField("Email",
                        validators=[InputRequired(), Email(), Length(max=50)])

    first_name = StringField("First Name",
                             validators=[InputRequired(), Length(max=30)])
    
    last_name = StringField("Last Name",
                             validators=[InputRequired(), Length(max=30)])


class LoginForm(FlaskForm):
    """User Login Form."""

    username = StringField("Username",
                           validators=[InputRequired(), Length(max=20)])

    password = PasswordField("Password",
                           validators=[InputRequired()])


class NoteForm(FlaskForm):
    """Adds and Edit a note for user."""

    title = StringField("Title",
                        validators=[InputRequired(), Length(max=100)])

    content = StringField("Content",
                        validators=[InputRequired()])