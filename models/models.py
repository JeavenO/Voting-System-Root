from flask_sqlalchemy import SQLAlchemy

# Initialize the SQLAlchemy database instance
db = SQLAlchemy()

# The User model stores voter credentials and profile information
class User(db.Model):
    __tablename__ = 'user' # Explicitly setting table name
    
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    
    # INCREASED: Hashed passwords are long strings; 500 characters prevents truncation
    password = db.Column(db.String(500), nullable=False)
    
    # One-to-many relationship: One user can have many votes
    votes = db.relationship('Vote', backref='voter', lazy=True)

# The Vote model keeps track of which user voted for which candidate
class Vote(db.Model):
    __tablename__ = 'vote' # Explicitly setting table name
    
    id = db.Column(db.Integer, primary_key=True)
    candidate_name = db.Column(db.String(100), nullable=False)
    
    # Foreign key establishing the link to the specific user
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)