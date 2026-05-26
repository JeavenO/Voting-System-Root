from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database instance
# We keep this separate from the app to avoid circular import issues
db = SQLAlchemy()

# The User model stores voter credentials and profile information
class User(db.Model):
    # Primary key identifier for every user
    id = db.Column(db.Integer, primary_key=True)
    # The unique username used for authentication
    username = db.Column(db.String(80), unique=True, nullable=False)
    # The hashed password string (never store plain-text!)
    password = db.Column(db.String(120), nullable=False)
    # One-to-many relationship: One user can have many votes (though we restrict to 1)
    votes = db.relationship('Vote', backref='voter', lazy=True)

# The Vote model keeps track of which user voted for which candidate
class Vote(db.Model):
    # Unique identifier for the vote record
    id = db.Column(db.Integer, primary_key=True)
    # The specific candidate chosen by the user
    candidate_name = db.Column(db.String(100), nullable=False)
    # Foreign key establishing the link to the specific user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)