from flask import request, jsonify
# Imports for secure password handling
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User, Vote 

def register_routes(app):
    """Function to register all API routes to the main Flask application."""
    
    @app.route('/register', methods=['POST'])
    def register():
        """Handles new user registration."""
        try:
            data = request.get_json()
            # Validate that user provided both fields
            if not data or 'username' not in data or 'password' not in data:
                return jsonify({"error": "Missing fields"}), 400

            # Check if user already exists in the database
            if User.query.filter_by(username=data['username']).first():
                return jsonify({"error": "User already exists"}), 409

            # Generate a secure hash from the plain password provided
            hashed_pw = generate_password_hash(data['password'])
            # Create the User object with the hashed password
            new_user = User(username=data['username'], password=hashed_pw)
            
            # Save to the database
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully!"}), 201
        except Exception as e:
            # Catch-all for database or server errors
            return jsonify({"error": "Internal server error", "details": str(e)}), 500

    @app.route('/vote', methods=['POST'])
    def cast_vote():
        """Handles authenticated voting."""
        try:
            data = request.get_json()
            # Ensure all required credentials and voting info are present
            if not data or not all(k in data for k in ('username', 'password', 'candidate')):
                return jsonify({"error": "Missing required data"}), 400

            # Verify the user exists
            user = User.query.filter_by(username=data['username']).first()
            # Check password against the stored hash
            if not user or not check_password_hash(user.password, data['password']):
                return jsonify({"error": "Invalid credentials"}), 401

            # Check if the user has already cast a vote to enforce fairness
            if Vote.query.filter_by(user_id=user.id).first():
                return jsonify({"error": "Vote already cast"}), 403

            # Record the new vote
            new_vote = Vote(candidate_name=data['candidate'], user_id=user.id)
            db.session.add(new_vote)
            db.session.commit()
            return jsonify({"message": "Vote recorded"}), 201
        except Exception as e:
            return jsonify({"error": "Failed to cast vote", "details": str(e)}), 500

    @app.route('/results', methods=['GET'])
    def get_results():
        """Aggregates and returns the total vote count per candidate."""
        try:
            all_votes = Vote.query.all()
            results = {}
            # Loop through all votes and tally them into the dictionary
            for v in all_votes:
                results[v.candidate_name] = results.get(v.candidate_name, 0) + 1
            return jsonify(results), 200
        except Exception as e:
            return jsonify({"error": "Could not retrieve results", "details": str(e)}), 500