# tasks.py
import uuid
from flask import Blueprint, request, jsonify
from permissions.utils import user_logged_in, protected_update
from models import db, Task, UserTask

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/all', methods=['GET'])
def get_all_tasks():
    """
    /tasks/all - GET
    """
    tasks = Task.query.all()
    tasks_list = []
    for t in tasks:
        tasks_list.append({
            "id": t.id,
            "name": t.name,
            "deadline": t.deadline.isoformat() if t.deadline else None,
            "description": t.description
        })
    return jsonify({"tasks": tasks_list}), 200


@tasks_bp.route('/tasks/create', methods=['POST'])
@user_logged_in(is_admin=True)
def create_task():
    """
    /tasks/create - POST
    Request: { "task": Task }
    """
    data = request.get_json() or {}
    task_data = data.get("task")
    if not task_data:
        return jsonify({"success": False, "message": "No task data"}), 400

    task_id = uuid.uuid4().hex
    
    new_task = Task(
        id=task_id,
        name=task_data.get("name"),
        created_by=task_data.get("created_by"),
        reward=task_data.get("reward", 0.0),
        deadline=task_data.get("deadline"),
        user_limit=task_data.get("user_limit", 0),
        description=task_data.get("description"),
        require_review=task_data.get("require_review", False),
        require_proof=task_data.get("require_proof", False),
        is_recurring=task_data.get("is_recurring", False),
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"success": True, "id": task_id, "message": "Task created"}), 201


@tasks_bp.route('/tasks/update', methods=['PATCH'])
@user_logged_in(is_admin=True)
def update_task():
    """
    /tasks/update - PATCH
    Request: { "task": Task }
    """
    data = request.get_json() or {}
    task_data = data.get("task", {})
    task_id = task_data.get("id")
    if not task_id:
        return jsonify({"success": False, "message": "Task ID is required"}), 400

    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    task.name = task_data.get("name", task.name)
    task.reward = task_data.get("reward", task.reward)
    task.deadline = task_data.get("deadline", task.deadline)
    task.user_limit = task_data.get("user_limit", task.user_limit)
    task.description = task_data.get("description", task.description)
    task.require_review = task_data.get("require_review", task.require_review)
    task.require_proof = task_data.get("require_proof", task.require_proof)
    task.is_recurring = task_data.get("is_recurring", task.is_recurring)

    db.session.commit()
    return jsonify({"success": True, "message": "Task updated"}), 200


@tasks_bp.route('/tasks/delete', methods=['DELETE'])
@user_logged_in(is_admin=True)
def delete_task():
    """
    /tasks/delete - DELETE
    Request: { "id": str }
    """
    data = request.get_json() or {}
    task_id = data.get("id")
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    db.session.delete(task)
    db.session.commit()
    return jsonify({"success": True, "message": "Task deleted"}), 200


@tasks_bp.route('/tasks/apply', methods=['POST'])
@user_logged_in()
def apply_task():
    """
    /tasks/apply - POST
    Request JSON: { "id": <task_id>, "uid": <user_id> }
      - 'id' is the ID of the Task
      - 'uid' is the ID of the User
    """
    data = request.get_json() or {}
    task_id = data.get("id")
    user_id = data.get("uid")

    # Validate input
    if not task_id or not user_id:
        return jsonify({"success": False, "message": "Task ID and User ID are required"}), 400

    # Optionally, you may check if the Task or User exist in DB
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    usertask_id = uuid.uuid4().hex

    new_user_task = UserTask(
        id=usertask_id,
        uid=user_id,
        task=task_id,
        status='APPLIED',
        proof_of_completion=None,
        admin_comment=None
    )

    db.session.add(new_user_task)
    db.session.commit()

    return jsonify({
        "success": True,
        "id": usertask_id,
        "message": "Task application successful"
    }), 201


@tasks_bp.route('/tasks/cancel', methods=['POST'])
@user_logged_in()
def cancel_task():
    """
    /tasks/cancel - POST
    Request JSON: { "id": <usertask_id> }
      - 'id' is the ID of the UserTask
    """
    data = request.get_json() or {}
    usertask_id = data.get("id")

    # Validate input
    if not usertask_id:
        return jsonify({"success": False, "message": "UserTask ID is required"}), 400

    # Find the usertask record
    usertask = UserTask.query.filter_by(id=usertask_id).first()
    if not usertask:
        return jsonify({"success": False, "message": "UserTask not found"}), 404
    
    db.session.delete(usertask)
    db.session.commit()

    return jsonify({
        "success": True,
        "message": "Task canceled successfully"
    }), 200
