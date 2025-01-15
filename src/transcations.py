# transactions.py
import uuid
from flask import Blueprint, request, jsonify
from permissions.utils import user_logged_in, protected_update
from models import db, Transaction

transactions_bp = Blueprint("transactions", __name__)

def transaction_to_dict(tx):
    """Helper function to convert a Transaction object to a dict."""
    return {
        "id": tx.id,
        "item": tx.item,
        "uid": tx.uid,
        "quantity": tx.quantity,
        "status": tx.status
    }

@transactions_bp.route("/transactions/all", methods=["GET"])
def get_all_transactions():
    """
    GET /transactions/all
    Returns:
        {
            "transactions": List[TransactionDict]
        }
    """
    transactions = Transaction.query.all()
    tx_list = [transaction_to_dict(tx) for tx in transactions]
    return jsonify({"transactions": tx_list}), 200

@transactions_bp.route("/transactions/<string:id>", methods=["POST"])
@user_logged_in()
def get_transaction(id):
    """
    POST /transactions/<id>
    Returns transcation of the specified transaction id

    Request Body: {}
    Response:
        {
            "transaction": TransactionDict
        }
    """
    tx = Transaction.query.filter_by(id=id).first()
    return jsonify({"transaction": transaction_to_dict(tx)}), 200


@transactions_bp.route("/transactions/users/<string:uid>", methods=["POST"])
@user_logged_in()
def get_user_transactions(uid):
    """
    POST /transactions/<uid>
    Returns all transactions associated with a specific user ID.

    Request Body: {}
    Response:
        {
            "transactions": List[TransactionDict]
        }
    """
    transactions = Transaction.query.filter_by(uid=uid).all()
    tx_list = [transaction_to_dict(tx) for tx in transactions]
    return jsonify({"transactions": tx_list}), 200


@transactions_bp.route("/transactions/update", methods=["PATCH"])
@user_logged_in(is_admin=True)
def update_transaction():
    """
    PATCH /transactions/update
    Request:
    {
       "transaction": {
          "id": <str>,
          "item": <str>,   (optional)
          "uid": <str>,    (optional)
          "quantity": <int>, (optional)
          "status": <str>  (optional)
       }
    }
    Response:
    {
        "success": <bool>,
        "message": <str>
    }
    """
    data = request.get_json() or {}
    tx_data = data.get("transaction") or {}

    if not tx_data:
        return jsonify({"success": False, "message": "No transaction data provided"}), 400

    tx_id = tx_data.get("id")
    if not tx_id:
        return jsonify({"success": False, "message": "Transaction ID is required"}), 400

    # Find existing transaction
    transaction = Transaction.query.filter_by(id=tx_id).first()
    if not transaction:
        return jsonify({"success": False, "message": "Transaction not found"}), 404

    # Update fields if provided
    # (You may add your own validation or business rules here)
    new_item = tx_data.get("item")
    if new_item is not None:
        transaction.item = new_item

    new_uid = tx_data.get("uid")
    if new_uid is not None:
        transaction.uid = new_uid

    new_quantity = tx_data.get("quantity")
    if new_quantity is not None:
        transaction.quantity = new_quantity

    new_status = tx_data.get("status")
    if new_status is not None:
        transaction.status = new_status

    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Transaction updated successfully"
    }), 200
