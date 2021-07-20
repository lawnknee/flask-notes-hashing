from flask import Flask, redirect, render_template, request,
from flask_bcrypt import Bcrypt
from models import db, connect_db, User
from forms import RegisterForm
from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql: // /flask_notes
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# move this out later
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def redirect_register():
    """Redirect to register page"""
    return redirect("/register")


@app.route("/register",  methods=["GET", "POST"])
def show_register_form():
    """ Displays register Forms with fields
    username, password, email, first_name, and last_name. 
    Registers user after submit
    """

    form = RegisterForm()

    if form.validate_on_submit():

        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data

        new_user = User(username, password, email, first_name, last_name)

        db.session.add(new_user)
        db.session.commit()

        redirect("/secret")

    else:
        render_template("register_user.html", form=form)
