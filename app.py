import os
from flask import Flask
from flask_cors import CORS 
from dotenv import load_dotenv
from models.models import db
from routes.auth import register_routes

# 1. Load environment variables
load_dotenv(override=True)

# 2. Initialize App
app = Flask(__name__)

# 3. Security: Configure CORS
# In production, specify your frontend origin instead of '*' for better security
CORS(app, resources={r"/*": {"origins": "*"}})

# 4. Database Config
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# Added: Set a secret key for session management/security
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'default-dev-secret-key')

# 5. Initialize Database
db.init_app(app)

# 6. Register Routes
register_routes(app)

# 7. Root Health Check
@app.route('/')
def home():
    return {"status": "success", "message": "Voting System API is online"}

# 8. Global Error Handler (Added for better debugging)
@app.errorhandler(404)
def not_found(e):
    return {"error": "Resource not found"}, 404

# 9. Main Execution
if __name__ == '__main__':
    with app.app_context():
        # Creates tables defined in models.py
        db.create_all()
        print("--- Database initialized successfully ---")
    
    # Use debug=True for development (auto-reloads on changes)
    app.run(port=5000, debug=True)