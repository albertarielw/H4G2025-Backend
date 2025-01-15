# tasks.py
import uuid
import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user
from models import db, Task, TaskRequest, Log

from permissions.utils import user_logged_in
from common.utils import create_user_tasks

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
def create_task():
    """
    /tasks/create - POST
    Request: { "task": Task }
    """
    data = request.get_json() or {}
    task_data = data.get("task")
    if not task_data:
        return jsonify({"success": False, "message": "No task data"}), 400

    new_task = Task(
        id=task_data.get("id"),
        name=task_data.get("name"),
        created_by=task_data.get("created_by"),
        reward=task_data.get("reward", 0.0),
        deadline=task_data.get("deadline"),   # format: "YYYY-MM-DD HH:MM:SS+00"
        user_limit=task_data.get("user_limit", 0),
        description=task_data.get("description"),
        require_review=task_data.get("require_review", False),
        require_proof=task_data.get("require_proof", False),
        is_recurring=task_data.get("is_recurring", False),
    )
    db.session.add(new_task)
    db.session.commit()
    return jsonify({"success": True, "message": "Task created"}), 201


@tasks_bp.route('/tasks/update', methods=['PATCH'])
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


@tasks_bp.route("/tasks/requests", methods=["POST"])
@user_logged_in()
def request_task():
    request_data = request.get_json()

    if current_user.cat == "ADMIN":
        return jsonify({"success": False, "message": "Please create tasks through the admin portal instead."}), 403

    end_time = request_data.get("end_time")
    if end_time < datetime.datetime.now():
        return jsonify({"success": False, "message": "End time must be in the future."}), 400

    task_request = TaskRequest(
        id=uuid.uuid4().hex,
        created_by=current_user.uid,
        name=request_data.get("name"),
        description=request_data.get("description"),
        reward=request_data.get("reward", 0.0),
        status="PENDING",
        start_time=request_data.get("start_time"),
        end_time=end_time,
        recurrence_interval=request_data.get("recurrence_interval"),
    )
    db.session.add(task_request)
    db.session.commit()
    return jsonify({"success": True, "message": "Task request created"}), 201


@tasks_bp.route("/tasks/requests/<string:request_id>/review", methods=["POST"])
@user_logged_in(is_admin=True)
def review_task_request(request_id):
    """
    /tasks/requests/<request_id>/review - POST
    Request: { "will_approve": bool, "comment": str, "require_review": bool, "require_proof": bool }
    """
    data = request.get_json() or {}
    if not (will_approve := data.get("will_approve")):
        return jsonify({"success": False, "message": "Please pass the will_approve argument."}), 400

    task_request = TaskRequest.query.filter_by(id=request_id).first()
    if not task_request:
        return jsonify({"success": False, "message": "Task request not found"}), 404

    if will_approve:
        task_request.status = "APPROVED"
        task_request.comment = data.get("comment")
        new_task = Task(
            id=uuid.uuid4().hex,
            name=task_request.name,
            created_by=current_user.uid,
            reward=task_request.reward,
            start_time=task_request.start_time,
            end_time=task_request.end_time,
            recurrence_interval=task_request.recurrence_interval,
            description=task_request.description,
            require_review=data.get("require_review"),
            require_proof=data.get("require_proof"),
        )
        user_tasks = create_user_tasks(new_task, task_request.created_by)
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"Admin {current_user.uid} approved task request {task_request.id}",
        )
        db.session.add(new_task)
        db.session.add_all(user_tasks)
    else:
        task_request.status = "REJECTED"
        task_request.comment = data.get("comment")
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"Admin {current_user.uid} rejected task request {task_request.id}",
        )
    db.session.add(log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task request reviewed"}), 20


@tasks_bp.route("/tasks/apply", methods=["POST"])
def apply_task():
    """
    /tasks/apply - POST
    Request: { "id": str, "uid": str }
    """
    data = request.get_json() or {}
    return jsonify({"success": True, "message": "Apply not yet implemented"}), 200


@tasks_bp.route('/tasks/cancel', methods=['POST'])
def cancel_task():
    """
    /tasks/cancel - POST
    Request: { "id": str, "uid": str }
    """
    data = request.get_json() or {}
    return jsonify({"success": True, "message": "Cancel not yet implemented"}), 200
