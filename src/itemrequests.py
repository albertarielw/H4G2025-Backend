# itemrequests.py
from flask import Blueprint, request, jsonify
from models import db, ItemRequest
from permissions.utils import user_logged_in
import uuid

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
@user_logged_in()
def create_itemrequest():
    """
    /itemrequests/create - POST
    Request: { "itemrequest": { ... } }
    """
    data = request.get_json() or {}
    ir_data = data.get("itemrequest", {})
    if not ir_data:
        return jsonify({"success": False, "message": "No itemrequest data"}), 400

    ir_id = uuid.uuid4().hex

    new_ir = ItemRequest(
        id=ir_id,
        requested_by=ir_data.get("requested_by"),
        description=ir_data.get("description")
    )
    db.session.add(new_ir)
    db.session.commit()
    return jsonify({"success": True, "id": ir_id, "message": "ItemRequest created"}), 201


@itemrequests_bp.route('/itemrequests/update', methods=['PATCH'])
@user_logged_in()
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

@itemrequests_bp.route('/itemrequests/<string:ir_id>/delete', methods=['DELETE'])
@user_logged_in()
def delete_itemrequest(ir_id):
    """
    /itemrequests/<ir_id>/delete - DELETE
    Request: {}
    """
    # Fetch the ItemRequest by its ID
    item_request = ItemRequest.query.filter_by(id=ir_id).first()
    if not item_request:
        return jsonify({"success": False, "message": "ItemRequest not found"}), 404

    # Delete the ItemRequest
    db.session.delete(item_request)
    db.session.commit()

    return jsonify({"success": True, "message": f"ItemRequest {ir_id} deleted successfully"}), 200
