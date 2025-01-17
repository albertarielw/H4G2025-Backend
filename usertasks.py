# usertasks.py
from flask import Blueprint, request, jsonify
from permissions.utils import user_logged_in, protected_update
from models import db, UserTask

usertasks_bp = Blueprint('usertasks', __name__)

@usertasks_bp.route('/usertasks/all', methods=['GET'])
@user_logged_in()
def get_all_usertasks():
    """
    /usertasks/all - GET
    Retrieve all usertasks.
    """
    usertasks = UserTask.query.all()
    output = []
    for ut in usertasks:
        output.append({
            "id": ut.id,
            "uid": ut.uid,
            "task": ut.task,
            "start_time": ut.start_time.isoformat() if ut.start_time else None,
            "end_time": ut.end_time.isoformat() if ut.end_time else None,
            "status": ut.status,
            "admin_comment": ut.admin_comment,
        })
    return jsonify({"usertasks": output}), 200


@usertasks_bp.route('/usertasks/update', methods=['PATCH'])
@user_logged_in(is_admin=True)
def update_usertask():
    """
    /usertasks/update - PATCH
    Request JSON:
    {
        "usertask": {
            "id": str,                 -- Required
            "status": str (optional),
            "start_time": str (ISO8601, optional),
            "end_time": str (ISO8601, optional),
            "admin_comment": str (optional)
        }
    }
    """
    data = request.get_json() or {}
    ut_data = data.get("usertask", {})
    ut_id = ut_data.get("id")
    if not ut_id:
        return jsonify({"success": False, "message": "UserTask ID is required"}), 400

    usertask = UserTask.query.filter_by(id=ut_id).first()
    if not usertask:
        return jsonify({"success": False, "message": "UserTask not found"}), 404

    # Update the fields provided in the request
    usertask.status = ut_data.get("status", usertask.status)
    usertask.start_time = ut_data.get("start_time", usertask.start_time)
    usertask.end_time = ut_data.get("end_time", usertask.end_time)
    usertask.admin_comment = ut_data.get("admin_comment", usertask.admin_comment)

    db.session.commit()
    return jsonify({"success": True, "message": "UserTask updated"}), 200


@usertasks_bp.route('/usertasks/delete', methods=['DELETE'])
@user_logged_in()
def delete_usertask():
    """
    /usertasks/delete - DELETE
    Request JSON:
    { "id": str }  -- The ID of the UserTask to delete
    """
    data = request.get_json() or {}
    ut_id = data.get("id")
    if not ut_id:
        return jsonify({"success": False, "message": "UserTask ID is required"}), 400

    usertask = UserTask.query.filter_by(id=ut_id).first()
    if not usertask:
        return jsonify({"success": False, "message": "UserTask not found"}), 404

    db.session.delete(usertask)
    db.session.commit()
    return jsonify({"success": True, "message": "UserTask deleted"}), 200
