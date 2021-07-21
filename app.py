from flask import Flask, redirect, render_template, session
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, NoteForm
from flask_debugtoolbar import DebugToolbarExtension
from werkzeug.exceptions import Unauthorized


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql:///flask_notes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
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
    
    if "username" in session:
        return redirect(f'/users/{session["username"]}')

    form = RegisterForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        email = form.email.data
        first_name = form.first_name.data
        last_name = form.last_name.data
        
        new_user = User.register(username, 
                                 password, 
                                 email, 
                                 first_name, 
                                 last_name)

        db.session.add(new_user)
        db.session.commit()
        session["username"] = new_user.username
        
        return redirect(f"/users/{username}")
    else:
        return render_template("register.html", form=form)


@app.route("/login",  methods=["GET", "POST"])
def handle_login_form():
    """Displays login form and handles user authentication."""
    
    if "username" in session:
        return redirect(f'/users/{session["username"]}')

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
            return render_template('login.html', form=form)
            
    else:
        return render_template("login.html", form=form)
    
    
@app.route('/users/<username>')
def user_homepage(username):
    """Displays current user's details and notes."""
    
    if "username" not in session or session["username"] != username:
        raise Unauthorized()
    # can turn into helper function?

    elif username == session["username"]:
        user = User.query.get_or_404(username)
        # notes = Note.query.filter_by(owner=username)
        notes = user.notes
        return render_template("user_homepage.html", 
                               user=user, 
                               notes=notes )
    

@app.route('/logout', methods=["POST"] )
def logout():
    """Logs current userout and redirects to homepage."""
    
    session.pop( "username" , None)

    return redirect("/")


@app.route('/users/<username>/delete', methods=["POST"] )
def destroy_user(username):
    """Deletes user & notes from database and redirects to register form"""

    user = User.query.get_or_404(username)
    
    Note.query.filter_by(owner=username).delete()

    db.session.delete(user)
    db.session.commit()

    session.pop("username" , None)

    return redirect("/")


########################### NOTES ##################################


@app.route('/users/<username>/notes/add', methods=["GET", "POST"] )
def notes_add_form(username):
    """Renders add note form and submits note."""

    form = NoteForm()

    if form.validate_on_submit():
        data = { k:v for k,v in form.data.items() if k != "csrf_token" }
        new_note = Note(**data, owner=username)

        db.session.add(new_note)
        db.session.commit()

        return redirect(f"/users/{username}")

    else:
        return render_template("new_note.html" , form=form, username=username)


@app.route('/notes/<note_id>/update', methods=["GET", "POST"] )
def notes_edit_form(note_id):
    """Renders edit note form and submits editted note."""
    
    note = Note.query.get_or_404(note_id)
    form = NoteForm(obj=note)
    
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner}")

    else:
        return render_template("edit_note.html" , form=form, note_id=note_id, username=note.owner )

@app.route("/notes/<note_id>/delete", methods=["POST"] ) 
def delete_note(note_id):
    """Deletes current note."""

    note = Note.query.get_or_404(note_id)
    username = note.owner
    
    db.session.delete(note)
    db.session.commit()

    return redirect(f"/users/{username}")