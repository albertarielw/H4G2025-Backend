# usertasks.py
from flask import Blueprint, request, jsonify
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


@usertasks_bp.route('/usertasks/add', methods=['POST'])
def add_usertask():
    """
    /usertasks/add - POST
    Request: { "usertask": UserTask }
    """
    data = request.get_json() or {}
    ut_data = data.get("usertask", {})
    if not ut_data:
        return jsonify({"success": False, "message": "No usertask data"}), 400

    new_ut = UserTask(
        uid=ut_data.get("uid"),
        task=ut_data.get("task"),
        status=ut_data.get("status", "APPLIED")
    )
    db.session.add(new_ut)
    db.session.commit()
    return jsonify({"success": True, "message": "UserTask added"}), 201


@usertasks_bp.route('/usertasks/update', methods=['PATCH'])
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

    usertask.uid = ut_data.get("uid", usertask.uid)
    usertask.task = ut_data.get("task", usertask.task)
    usertask.status = ut_data.get("status", usertask.status)

    db.session.commit()
    return jsonify({"success": True, "message": "UserTask updated"}), 200


@usertasks_bp.route('/usertasks/delete', methods=['DELETE'])
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
