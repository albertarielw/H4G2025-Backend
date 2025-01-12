# itemrequests.py
from flask import Blueprint, request, jsonify
from models import db, ItemRequest

itemrequests_bp = Blueprint('itemrequests', __name__)

@itemrequests_bp.route('/itemrequests/all', methods=['GET'])
def get_all_itemrequests():
    """
    /itemrequests/all - GET
    """
    requests = ItemRequest.query.all()
    output = []
    for ir in requests:
        output.append({
            "id": ir.id,
            "requested_by": ir.requested_by,
            "description": ir.description
        })
    return jsonify({"itemrequests": output}), 200


@itemrequests_bp.route('/itemrequests/create', methods=['POST'])
def create_itemrequest():
    """
    /itemrequests/create - POST
    Request: { "itemrequest": { ... } }
    """
    data = request.get_json() or {}
    ir_data = data.get("itemrequest", {})
    if not ir_data:
        return jsonify({"success": False, "message": "No itemrequest data"}), 400

    new_ir = ItemRequest(
        id=ir_data.get("id"),
        requested_by=ir_data.get("requested_by"),
        description=ir_data.get("description")
    )
    db.session.add(new_ir)
    db.session.commit()
    return jsonify({"success": True, "message": "ItemRequest created"}), 201


@itemrequests_bp.route('/itemrequests/update', methods=['PATCH'])
def update_itemrequest():
    """
    /itemrequests/update - PATCH
    Request: { "itemrequest": { ... } }
    """
    data = request.get_json() or {}
    ir_data = data.get("itemrequest", {})
    ir_id = ir_data.get("id")
    if not ir_id:
        return jsonify({"success": False, "message": "ItemRequest ID required"}), 400

    ir = ItemRequest.query.filter_by(id=ir_id).first()
    if not ir:
        return jsonify({"success": False, "message": "ItemRequest not found"}), 404

    ir.requested_by = ir_data.get("requested_by", ir.requested_by)
    ir.description = ir_data.get("description", ir.description)
    db.session.commit()
    return jsonify({"success": True, "message": "ItemRequest updated"}), 200
