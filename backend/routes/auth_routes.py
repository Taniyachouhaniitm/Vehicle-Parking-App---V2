from flask import Blueprint, request, jsonify
from models import db, User
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json

    if User.query.filter_by(username=data['username']).first():
        return jsonify({"msg": "Username already exists"}), 400

    if User.query.filter_by(email=data['email']).first():
        return jsonify({"msg": "Email already exists"}), 400

    user = User(
        username=data['username'],
        email=data['email'],
        fname=data['fname'],
        lname=data['lname'],
        password=generate_password_hash(data['password']),
        role_id=2  # user
    )
    db.session.add(user)
    db.session.commit()
    return jsonify({"msg": "User registered"}), 200


@auth_bp.route('/login', methods=['POST'])
def login():
    try:
        data = request.get_json()
        user = User.query.filter_by(email=data['email']).first()

        if not user or not check_password_hash(user.password, data['password']):
            return jsonify({"msg": "Invalid credentials"}), 401

        access_token = create_access_token(identity=str(user.id))
        
        return jsonify({
            "access_token": access_token,
            "role_id": user.role_id,
            "username": user.username,
            "email": user.email
        }), 200

    except Exception as e:
        print("LOGIN ERROR:", e)
        return jsonify({"msg": "Internal server error"}), 500
