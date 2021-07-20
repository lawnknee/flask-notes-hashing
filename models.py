"""Model for Flask Notes."""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)
    
class User(db.Model):
    """Flask Notes User."""
  
    __tablename__ = "users"
  
    username = db.Column(db.String(20),
                         nullable=False,
                         primary_key=True,
                         unique=True)
    
    password = db.Column(db.Text,
                         nullable=False)
    
    email = db.Column(db.String(50),
                      nullable=False,
                      unique=True)
    
    first_name = db.Column(db.String(30),
                           nullable=False)
    
    last_name = db.Column(db.String(30),
                          nullable=False)