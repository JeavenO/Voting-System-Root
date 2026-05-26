import os
from flask import Flask
from flask_cors import CORS # Import CORS to allow cross-origin requests from your frontend
from dotenv import load_dotenv
from models.models import db
from routes.auth import register_routes

# Load environment variables (like DATABASE_URL) from the .env file
load_dotenv(override=True)

# Initialize the main Flask application instance
app = Flask(__name__)

# Enable Cross-Origin Resource Sharing (CORS) 
# This allows your future frontend (e.g., HTML/JS) to communicate with this API
CORS(app)

# Configure the database connection using the URL stored in your environment
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
# Disable tracking of modifications to save memory and improve performance
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the SQLAlchemy database instance with the Flask app context
db.init_app(app)

# Register the API routes imported from your routes/auth.py module
register_routes(app)

# Root route to verify the API is running correctly
@app.route('/')
def home():
    """Welcome route to check API status."""
    return {"message": "Welcome to the Voting System API"}

# Entry point: ensures the script runs only when executed directly
if __name__ == '__main__':
    # Utilize the application context to safely create/verify database tables
    with app.app_context():
        # This will create any missing tables based on the models defined in models.py
        db.create_all()
        print("Database tables created/verified successfully.")
    
    # Run the development server on port 5000
    app.run(port=5000)