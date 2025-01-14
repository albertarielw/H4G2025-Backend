# items.py
import uuid

from flask import Blueprint, request, jsonify
from models import db, Item, User, Transaction
from permissions.utils import user_logged_in

items_bp = Blueprint('items', __name__)

@items_bp.route('/items/all', methods=['GET'])
def get_all_items():
    """
    /items/all - GET
    Returns all items.
    """
    items = Item.query.all()
    items_list = []
    for i in items:
        items_list.append({
            "id": i.id,
            "name": i.name,
            "stock": i.stock,
            "price": i.price,
            "description": i.description,
            "image": i.image,
        })
    return jsonify({"items": items_list}), 200


@items_bp.route('/items/<string:item_id>', methods=['GET'])
def get_item_by_id(item_id):
    """
    /items/${id} - GET
    """
    item = Item.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    return jsonify({
        "item": {
            "id": item.id,
            "name": item.name,
            "stock": item.stock,
            "price": item.price,
            "description": item.description,
            "image": item.image,
        }
    }), 200


@items_bp.route("/items/create", methods=["POST"])
@user_logged_in(is_admin=True)
def create_item():
    """
    /items/create - POST
    Request: { "item": Item }
    """
    data = request.get_json() or {}
    item_data = data.get("item")
    if not item_data:
        return jsonify({"success": False, "message": "No item data provided"}), 400

    new_item = Item(
        id=item_data.get("id"),
        name=item_data.get("name"),
        image=item_data.get("image"),  
        stock=item_data.get("stock", 0),
        price=item_data.get("price", 0),
        description=item_data.get("description"),
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Item created"}), 201


@items_bp.route("/items/update", methods=["PATCH"])
@user_logged_in(is_admin=True)
def update_item():
    """
    /items/update - PATCH
    Request: { "item": {id, name, stock, price, ...} }
    """
    data = request.get_json() or {}
    item_data = data.get("item", {})
    item_id = item_data.get("id")
    if not item_id:
        return jsonify({"success": False, "message": "Item ID required"}), 400

    item = Item.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    item.name = item_data.get("name", item.name)
    item.stock = item_data.get("stock", item.stock)
    item.price = item_data.get("price", item.price)
    item.description=item_data.get("description", item.description)
    item.image=item_data.get("image", item.image)
    db.session.commit()
    return jsonify({"success": True, "message": "Item updated"}), 200


@items_bp.route("/items/delete", methods=["DELETE"])
@user_logged_in(is_admin=True)
def delete_item():
    """
    /items/delete - DELETE
    Request: { "id": str }
    """
    data = request.get_json() or {}
    item_id = data.get("id")
    item = Item.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    db.session.delete(item)
    db.session.commit()
    return jsonify({"success": True, "message": "Item deleted"}), 200


@items_bp.route('/items/buy', methods=['POST'])
def buy_item():
    """
    /items/buy - POST
    Request: { "id": str, "quantity": int, "uid": str }
    """
    data = request.get_json() or {}
    item_id = data.get("id")
    quantity = data.get("quantity")
    user_id = data.get("uid")

    if not item_id or not quantity or not user_id:
        return jsonify({"success": False, "message": "Missing item_id, quantity, or user_id"}), 400

    # 1) Get the item
    item = Item.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    # 2) Check quantity vs. stock
    if quantity <= 0:
        return jsonify({"success": False, "message": "Invalid quantity"}), 400
    
    if quantity > item.stock:
        return jsonify({"success": False, "message": "Requested quantity exceeds available stock"}), 400

    # 3) Get the user
    user = User.query.filter_by(uid=user_id).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # 4) Check user credit vs. cost
    total_price = quantity * item.price
    if user.credit < total_price:
        return jsonify({"success": False, "message": "Insufficient credit"}), 400

    # At this point, we assume purchase is allowed to proceed
    try:
        # 5) Deduct stock
        item.stock = item.stock - quantity

        user.credit = user.credit - total_price

        # 6) Insert transaction
        transaction_id = str(uuid.uuid4())  # or any other logic for generating IDs
        new_transaction = Transaction(
            id=transaction_id,
            item=item_id,
            uid=user_id,
            quantity=quantity,
            status='AWAITING_CONF'  
        )
        db.session.add(new_transaction)

        db.session.commit()

        return jsonify({"success": True, "message": "Purchase successful", "transaction_id": transaction_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500


@items_bp.route('/items/preorder', methods=['POST'])
def preorder_item():
    """
    /items/buy - POST
    Request: { "id": str, "quantity": int, "uid": str }
    """
    data = request.get_json() or {}
    item_id = data.get("id")
    quantity = data.get("quantity")
    user_id = data.get("uid")

    if not item_id or not quantity or not user_id:
        return jsonify({"success": False, "message": "Missing item_id, quantity, or user_id"}), 400

    # 1) Get the item
    item = Item.query.filter_by(id=item_id).first()
    if not item:
        return jsonify({"success": False, "message": "Item not found"}), 404

    # 2) Check quantity
    if quantity <= 0:
        return jsonify({"success": False, "message": "Invalid quantity"}), 400

    # 3) Get the user
    user = User.query.filter_by(uid=user_id).first()
    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    # 4) Check user credit vs. cost
    total_price = quantity * item.price
    if user.credit < total_price:
        return jsonify({"success": False, "message": "Insufficient credit"}), 400

    # At this point, we assume purchase is allowed to proceed
    try:
        user.credit = user.credit - total_price

        # 5) Insert transaction
        transaction_id = str(uuid.uuid4())  # or any other logic for generating IDs
        new_transaction = Transaction(
            id=transaction_id,
            item=item_id,
            uid=user_id,
            quantity=quantity,
            status='PREORDER'  
        )
        db.session.add(new_transaction)

        db.session.commit()

        return jsonify({"success": True, "message": "Purchase successful", "transaction_id": transaction_id}), 200
    except Exception as e:
        db.session.rollback()
        return jsonify({"success": False, "message": f"Error: {str(e)}"}), 500
