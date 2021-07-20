from flask import Flask, redirect, render_template, request, session, flash
from models import db, connect_db, User
from forms import RegisterForm, LoginForm
from flask_debugtoolbar import DebugToolbarExtension



app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
# move this out later
app.config['SECRET_KEY'] = "SECRET!"
debug = DebugToolbarExtension(app)

connect_db(app)
db.create_all()


@app.route("/")
def redirect_register():
    """Redirect to register page."""
    return redirect("/register")


@app.route("/register",  methods=["GET", "POST"])
def handle_register_form():
    """ Displays register form with fields:
    username, password, email, first_name, and last_name. 
    Registers user after submit.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        # new_user = User(username=username, 
        #                 password=password, 
        #                 email=email, 
        #                 first_name=first_name, 
        #                 last_name=last_name)
        
        new_user = User.register(username, 
                                 password, 
                                 email, 
                                 first_name, 
                                 last_name)

        db.session.add(new_user)
        db.session.commit()
        
        return redirect("/login")
    
    else:
        return render_template("register.html", form=form)


@app.route("/login",  methods=["GET", "POST"])
def handle_login_form():

    form = LoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        
        current_user = User.authenticate(username, password)

        if current_user:
            session["username"] = current_user.username
            return redirect(f"/users/{username}")
        else:
            form.username.errors = ["Bad name/password"]
            
    else:
        return render_template("login.html", form=form)
    
@app.route('/users/<username>')
def user_homepage(username):
    
    if "username" not in session or session["username"] !=username:
        flash("You dont belong here ...  yet")
        return redirect("/")

    elif username == session["username"]:
        user = User.query.get(username)
        return render_template("user_homepage.html" , user=user )


    
    

@app.route('/logout', methods=["POST"] )
def logout():
    """ Log users out and redirects to homepage"""
    session.pop( "username" , None)

    return redirect("/")