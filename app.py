from flask import Flask, redirect, render_template, request, session, flash
from models import db, connect_db, User, Note
from forms import RegisterForm, LoginForm, NotesAddForm, NotesEditForm
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
        notes = Note.query.filter_by(owner=username)
        return render_template("user_homepage.html", 
                               user=user, 
                               notes=notes )
    

@app.route('/logout', methods=["POST"] )
def logout():
    """ Log users out and redirects to homepage"""
    session.pop( "username" , None)

    return redirect("/")


@app.route('/users/<username>/delete', methods=["POST"] )
def destroy_user(username):
    """Deletes user & notes from database and redirects to register form"""

    user = User.query.get_or_404(username)
    notes = Note.query.filter_by(owner=username)

    #  check later after we havd notes
    # db.session.delete(notes)
    db.session.delete(user)
    db.session.commit()

    session.pop( "username" , None)

    return redirect("/")





########################### NOTES ###########################################################

@app.route('/users/<username>/notes/add', methods=["GET", "POST"] )
def notes_add_form(username):
    """Renders add notes form and submits notes"""

    form = NotesAddForm()

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
    """Renders add notes form and submits notes"""

    
    note = Note.query.get(note_id)
    form = NotesAddForm(obj=note)
    
    if form.validate_on_submit():
        note.title = form.title.data
        note.content = form.content.data

        db.session.commit()

        return redirect(f"/users/{note.owner}")

    else:
        return render_template("edit_note.html" , form=form, note_id=note_id, username=note.owner )

@app.route("/notes/<note_id>/delete", methods=["POST"] ) 
def delete_note(note_id):
    """Deletes note"""

    note = Note.query.get_or_404(note_id)
    username = note.owner
    
    db.session.delete(note)
    db.session.commit()

    return redirect(f"/users/{username}")