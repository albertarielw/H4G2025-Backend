# items.py
from flask import Blueprint, request, jsonify
from models import db, Item

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
            "price": i.price
            # image omitted, or handle appropriately
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
            "price": item.price
        }
    }), 200


@items_bp.route('/items/create', methods=['POST'])
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
        image=None,  # handle base64 or file uploads if needed
        stock=item_data.get("stock", 0),
        price=item_data.get("price", 0)
    )
    db.session.add(new_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Item created"}), 201


@items_bp.route('/items/update', methods=['PATCH'])
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
    db.session.commit()
    return jsonify({"success": True, "message": "Item updated"}), 200


@items_bp.route('/items/delete', methods=['DELETE'])
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
    Request: { "id": str, "quantity": int }
    Creates or updates a transaction in the backend. 
    """
    # For simplicity, just a placeholder with success response
    data = request.get_json() or {}
    item_id = data.get("id")
    quantity = data.get("quantity")
    # Logic to reduce item stock, create transaction, etc.
    return jsonify({"success": True, "message": "Buy item not yet implemented"}), 200


@items_bp.route('/items/preorder', methods=['POST'])
def preorder_item():
    """
    /items/preorder - POST
    Request: { "id": str, "quantity": int }
    """
    # Placeholder
    data = request.get_json() or {}
    return jsonify({"success": True, "message": "Preorder not yet implemented"}), 200
