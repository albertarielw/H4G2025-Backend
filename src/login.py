# login.py
from flask import Blueprint, request, jsonify
from models import db, User
from flask_jwt_extended import create_access_token

login_bp = Blueprint('login', __name__)

@login_bp.route('/login', methods=['POST'])
def login():
    """
    /login - POST
    Request: { "email": str, "password": str }
    Response: { "success": bool, "message": str, "token": str }
    """
    data = request.get_json() or {}
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"success": False, "token": "", "message": "Missing credentials"}), 400

    user = User.query.filter_by(email=email, password=password).first()
    if not user:
        return jsonify({"success": False, "token": "", "message": "Invalid credentials"}), 401

    token = create_access_token(identity=user)

    # If login is successful, return uid
    return jsonify({"success": True, "token": token, "message": "Login successful"}), 200


@login_bp.route('/login/resetpassword', methods=['POST'])
def reset_password():
    """
    /login/resetpassword - POST
    Request: { "email": str, "password": str }
    """
    data = request.get_json() or {}
    email = data.get('email')
    new_password = data.get('password')

    if not email or not new_password:
        return jsonify({"success": False, "message": "Missing email or password"}), 400

    user = User.query.filter_by(email=email).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user.password = new_password
    db.session.commit()
    return jsonify({"success": True, "message": "Password reset successful"}), 200
