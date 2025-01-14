# usertasks.py
from flask import Blueprint, request, jsonify
from permissions.utils import user_logged_in, protected_update
from models import db, UserTask

usertasks_bp = Blueprint('usertasks', __name__)

@usertasks_bp.route('/usertasks/all', methods=['GET'])
def get_all_usertasks():
    """
    /usertasks/all - GET
    """
    usertasks = UserTask.query.all()
    output = []
    for ut in usertasks:
        output.append({
            "id": ut.id,
            "uid": ut.uid,
            "task": ut.task,
            "status": ut.status
        })
    return jsonify({"usertask": output}), 200

@usertasks_bp.route('/usertasks/update', methods=['PATCH'])
@user_logged_in()
def update_usertask():
    """
    /usertasks/update - PATCH
    Request: { "usertask": {...} }
    """
    data = request.get_json() or {}
    ut_data = data.get("usertask", {})
    ut_id = ut_data.get("id")
    if not ut_id:
        return jsonify({"success": False, "message": "UserTask ID required"}), 400

    usertask = UserTask.query.filter_by(id=ut_id).first()
    if not usertask:
        return jsonify({"success": False, "message": "UserTask not found"}), 404

    usertask.status = ut_data.get("status", usertask.status)
    usertask.proof_of_completion =  ut_data.get("proof_of_completion", usertask.proof_of_completion)
    usertask.admin_comment = ut_data.get("admin_comment", usertask.admin_comment)

    db.session.commit()
    return jsonify({"success": True, "message": "UserTask updated"}), 200


@usertasks_bp.route('/usertasks/delete', methods=['DELETE'])
@user_logged_in(is_admin=True)
def delete_usertask():
    """
    /usertasks/delete - DELETE
    Request: { "id": str }
    """
    data = request.get_json() or {}
    ut_id = data.get("id")
    usertask = UserTask.query.filter_by(id=ut_id).first()
    if not usertask:
        return jsonify({"success": False, "message": "UserTask not found"}), 404

    db.session.delete(usertask)
    db.session.commit()
    return jsonify({"success": True, "message": "UserTask deleted"}), 200
