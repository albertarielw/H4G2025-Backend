# tasks.py
import uuid
import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user
from models import db, Task, Log, UserTask, User

from permissions.utils import user_logged_in, protected_update
from common.utils import create_user_tasks, generate_update_diff

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/all', methods=['GET'])
def get_all_tasks():
    """
    /tasks/all - GET
    Retrieve all tasks.
    """
    tasks = Task.query.all()
    tasks_list = []
    for t in tasks:
        tasks_list.append({
            "id": t.id,
            "name": t.name,
            "created_by": t.created_by,
            "reward": str(t.reward),  # Convert Decimal to string or float if needed
            "start_time": t.start_time.isoformat() if t.start_time else None,
            "deadline": t.deadline.isoformat() if t.deadline else None,
            "is_recurring": t.is_recurring,
            "recurrence_interval": t.recurrence_interval,
            "description": t.description,
        })
    return jsonify({"tasks": tasks_list}), 200


@tasks_bp.route('/tasks/create', methods=['POST'])
@user_logged_in(is_admin=True)
def create_task():
    """
    /tasks/create - POST
    Request JSON: 
    {
        "task": {
            "name": str,
            "created_by": str,
            "reward": float (optional),
            "start_time": str (ISO8601 datetime, optional),
            "deadline": str (ISO8601 datetime, optional),
            "is_recurring": bool (optional),
            "recurrence_interval": int (optional),
            "description": str (optional)
        }
    }
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
        start_time=task_data.get("start_time"),
        deadline=task_data.get("deadline"),
        is_recurring=task_data.get("is_recurring", False),
        recurrence_interval=task_data.get("recurrence_interval"),
        description=task_data.get("description"),
    )

    db.session.add(new_task)
    db.session.commit()
    return jsonify({"success": True, "id": task_id, "message": "Task created"}), 201


@tasks_bp.route('/tasks/update', methods=['PATCH'])
@user_logged_in(is_admin=True)
def update_task():
    """
    /tasks/update - PATCH
    Request JSON:
    {
        "task": {
            "id": str,  -- Required
            "name": str (optional),
            "reward": float (optional),
            "start_time": str (ISO8601 datetime, optional),
            "deadline": str (ISO8601 datetime, optional),
            "is_recurring": bool (optional),
            "recurrence_interval": int (optional),
            "description": str (optional)
        }
    }
    """
    data = request.get_json() or {}
    task_data = data.get("task", {})
    task_id = task_data.get("id")
    if not task_id:
        return jsonify({"success": False, "message": "Task ID is required"}), 400

    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    # Update only the fields that are provided
    task.name = task_data.get("name", task.name)
    task.reward = task_data.get("reward", task.reward)
    task.start_time = task_data.get("start_time", task.start_time)
    task.deadline = task_data.get("deadline", task.deadline)
    task.is_recurring = task_data.get("is_recurring", task.is_recurring)
    task.recurrence_interval = task_data.get("recurrence_interval", task.recurrence_interval)
    task.description = task_data.get("description", task.description)

    db.session.commit()
    return jsonify({"success": True, "message": "Task updated"}), 200


@tasks_bp.route('/tasks/delete', methods=['DELETE'])
@user_logged_in(is_admin=True)
def delete_task():
    """
    /tasks/delete - DELETE
    Request JSON:
    { "id": str }  -- The ID of the task to delete
    """
    data = request.get_json() or {}
    task_id = data.get("id")
    if not task_id:
        return jsonify({"success": False, "message": "Task ID is required"}), 400

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
    Apply for a task.
    Request JSON:
    {
        "uid": str,  # User ID of the applicant
        "id": str    # Task ID of the task being applied for
    }
    """
    data = request.get_json() or {}
    user_id = data.get("uid")
    task_id = data.get("id")

    if not user_id or not task_id:
        return jsonify({"success": False, "message": "Both uid and id are required"}), 400

    # Fetch the user and task
    user = User.query.filter_by(uid=user_id).first()
    task = Task.query.filter_by(id=task_id).first()

    if not user:
        return jsonify({"success": False, "message": "User not found"}), 404

    if not task:
        return jsonify({"success": False, "message": "Task not found"}), 404

    # Generate a new UserTask entry
    usertask_id = uuid.uuid4().hex
    new_usertask = UserTask(
        id=usertask_id,
        uid=user_id,
        task=task_id,
        start_time=task.start_time,  # Use the task's start time
        end_time=task.deadline,      # Use the task's deadline
        status="APPLIED",            # Default status
        admin_comment=None           # No admin comment at creation
    )

    # Save the new UserTask entry to the database
    db.session.add(new_usertask)

    # Optionally log the event
    log_entry = Log(
        id=uuid.uuid4().hex,
        cat="USERTASK",
        uid=user_id,
        description=f"User {user_id} applied for task {task_id}"
    )
    db.session.add(log_entry)

    # Commit all changes
    db.session.commit()

    return jsonify({"success": True, "message": "Task application successful", "usertask_id": usertask_id}), 201
