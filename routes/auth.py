from flask import request, jsonify
from werkzeug.security import generate_password_hash, check_password_hash
from models.models import db, User, Vote 

def register_routes(app):
    """Registers all API routes to the Flask application."""
    
    # --- AUTHENTICATION ROUTES ---

    @app.route('/register', methods=['POST'])
    def register():
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'password' not in data:
                return jsonify({"error": "Missing fields"}), 400

            if User.query.filter_by(username=data['username']).first():
                return jsonify({"error": "User already exists"}), 409

            hashed_pw = generate_password_hash(data['password'])
            new_user = User(username=data['username'], password=hashed_pw)
            
            db.session.add(new_user)
            db.session.commit()
            return jsonify({"message": "User registered successfully!"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Internal server error", "details": str(e)}), 500

    @app.route('/login', methods=['POST'])
    def login():
        """Handles user login."""
        try:
            data = request.get_json()
            if not data or 'username' not in data or 'password' not in data:
                return jsonify({"error": "Missing credentials"}), 400

            user = User.query.filter_by(username=data['username']).first()
            
            # Verify user exists and password matches the hash
            if user and check_password_hash(user.password, data['password']):
                return jsonify({"message": "Login successful!"}), 200
            
            return jsonify({"error": "Invalid username or password"}), 401
        except Exception as e:
            return jsonify({"error": "Login failed", "details": str(e)}), 500

    # --- VOTING ROUTES ---

    @app.route('/vote', methods=['POST'])
    def cast_vote():
        try:
            data = request.get_json()
            if not data or not all(k in data for k in ('username', 'password', 'candidate')):
                return jsonify({"error": "Missing required data"}), 400

            user = User.query.filter_by(username=data['username']).first()
            if not user or not check_password_hash(user.password, data['password']):
                return jsonify({"error": "Invalid credentials"}), 401

            if Vote.query.filter_by(user_id=user.id).first():
                return jsonify({"error": "Vote already cast"}), 403

            new_vote = Vote(candidate_name=data['candidate'], user_id=user.id)
            db.session.add(new_vote)
            db.session.commit()
            return jsonify({"message": "Vote recorded"}), 201
        except Exception as e:
            db.session.rollback()
            return jsonify({"error": "Failed to cast vote", "details": str(e)}), 500

    @app.route('/results', methods=['GET'])
    def get_results():
        try:
            all_votes = Vote.query.all()
            results = {}
            for v in all_votes:
                results[v.candidate_name] = results.get(v.candidate_name, 0) + 1
            return jsonify(results), 200
        except Exception as e:
            return jsonify({"error": "Could not retrieve results", "details": str(e)}), 500