# users.py
import uuid

from flask import Blueprint, request, jsonify
from models import db, User, Task, Transaction

from permissions.utils import user_logged_in, protected_update

users_bp = Blueprint('users', __name__)


@users_bp.route("/users/<string:uid>", methods=["GET"])
def get_user_by_uid(uid):
    """
    /users/${uid} - GET
    Returns user details, tasks (empty if admin), transactions (empty if admin).
    """
    print(uid)
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # If user is an Admin, tasks & transactions in response must be empty
    tasks = []
    transactions = []
    if user.cat.lower() == 'user':
        # For normal user: let's assume tasks and transactions are everything
        tasks = Task.query.all()  # or tasks specifically assigned, etc.
        transactions = Transaction.query.filter_by(uid=user.uid).all()

    # Convert tasks to simple dict
    tasks_data = []
    for t in tasks:
        tasks_data.append({
            "id": t.id,
            "name": t.name,
            "created_by": t.created_by,
            "reward": t.reward,
            "deadline": t.deadline,
            "user_limit": t.user_limit,
            "description": t.description,
            "require_review": t.require_review,
            "require_proof": t.require_proof,
            "is_recurring": t.is_recurring,
        })

    trans_data = []
    for tr in transactions:
        trans_data.append({
            "id": tr.id,
            "item": tr.item,
            "uid": tr.uid,
            "quantity": tr.quantity,
            "status": tr.status
        })

    response = {
        "user": {
            "uid": user.uid,
            "name": user.name,
            "email": user.email,
            "credit": float(user.credit),
            "cat": user.cat
        },
        "tasks": tasks_data,
        "transactions": trans_data
    }
    return jsonify(response), 200


@users_bp.route("/users/add", methods=["POST"])
@user_logged_in(is_admin=True)
def add_user():
    """
    /users/add - POST
    Request: { "user": {uid, name, cat, email, password, credit} }
    """
    data = request.get_json()
    user_data = data.get("user", {})
    if not user_data:
        return jsonify({"success": False, "message": "No user data found"}), 400

    # Quick check if user already exists
    existing_user = User.query.filter_by(email=user_data.get('email')).first()
    if existing_user:
        return jsonify({"success": False, "message": "User already exists"}), 400

    new_user = User(
        uid=uuid.uuid4().hex,
        name=user_data.get("name"),
        cat=user_data.get("cat", "USER"),
        email=user_data.get("email"),
        password=user_data.get("password"),
        credit=user_data.get("credit", 0.0),
    )
    db.session.add(new_user)
    db.session.commit()

    return jsonify({"success": True, "message": "User added successfully"}), 201


@users_bp.route("/users/update", methods=["PATCH"])
@user_logged_in()
def update_user():
    """
    /users/update - PATCH
    Request: { "user": {...fields...} }
    """
    data = request.get_json()
    user_data = data.get("user", {})
    if not user_data:
        return jsonify({"success": False, "message": "No user data in request"}), 400

    uid = user_data.get("uid")
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # Update fields
    protected_update(user, "name", user_data)
    protected_update(user, "cat", user_data, admin_only=True)
    protected_update(user, "email", user_data, admin_only=True)
    protected_update(user, "password", user_data, admin_only=True)
    protected_update(user, "credit", user_data, admin_only=True)
    protected_update(user, "is_active", user_data, admin_only=True)
    db.session.commit()
    return jsonify({"success": True, "message": "User updated"}), 200


@users_bp.route("/users/suspend", methods=["PATCH"])
@user_logged_in(is_admin=True)
def suspend_user():
    """
    /users/suspend - PATCH
    Request: { "uid": str }
    """
    data = request.get_json()
    uid = data.get("uid")
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    user.is_active = False
    db.session.commit()

    return jsonify({"success": True, "message": f"User {uid} suspended"}), 200


@users_bp.route("/users/delete", methods=["DELETE"])
@user_logged_in(is_admin=True)
def delete_user():
    """
    /users/delete - DELETE
    Request: { "uid": str }
    """
    data = request.get_json()
    uid = data.get("uid")
    user = User.query.filter_by(uid=uid).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    db.session.delete(user)
    db.session.commit()
    return jsonify({"success": True, "message": f"User {uid} deleted"}), 200
