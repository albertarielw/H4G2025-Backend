# tasks.py
import uuid
import datetime

from flask import Blueprint, request, jsonify
from flask_jwt_extended import current_user
from models import db, Task, TaskRequest, Log, TaskPosting, TaskApplication, UserTask, User

from permissions.utils import user_logged_in, protected_update
from common.utils import create_user_tasks, generate_update_diff

tasks_bp = Blueprint('tasks', __name__)

@tasks_bp.route('/tasks/all', methods=['GET'])
def get_all_tasks():
    """
    /tasks/all - GET
    """
    tasks = Task.query.all()
    tasks_list = []
    for t in tasks:
        tasks_list.append(
            {
                "id": t.id,
                "name": t.name,
                "created_by": t.created_by,
                "reward": t.reward,
                "start_time": t.start_time,
                "end_time": t.end_time,
                "recurrence_interval": t.recurrence_interval,
                "description": t.description,
                "require_review": t.require_review,
                "require_proof": t.require_proof,
            }
        )
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
        start_time=task_data.get("start_time"),
        end_time=task_data.get("end_time"),
        recurrence_interval=task_data.get("recurrence_interval"),
        user_limit=task_data.get("user_limit", 0),
        description=task_data.get("description"),
        require_review=task_data.get("require_review", False),
        require_proof=task_data.get("require_proof", False),
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
    task.start_time = task_data.get("start_time", task.start_time)
    task.end_time = task_data.get("end_time", task.end_time)
    task.recurrence_interval = task_data.get("recurrence_interval", task.recurrence_interval)
    task.user_limit = task_data.get("user_limit", task.user_limit)
    task.description = task_data.get("description", task.description)
    task.require_review = task_data.get("require_review", task.require_review)
    task.require_proof = task_data.get("require_proof", task.require_proof)

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


## TASK REQUESTS ##
@tasks_bp.route("/tasks/requests/all", methods=["GET"])
def get_all_requests():
    """
    /tasks/requests/all - GET
    """
    requests = TaskRequest.query.all()
    requests_list = []
    for r in requests:
        requests_list.append(
            {
                "id": r.id,
                "name": r.name,
                "description": r.description,
                "reward": r.reward,
                "status": r.status,
                "start_time": r.start_time,
                "end_time": r.end_time,
                "recurrence_interval": r.recurrence_interval,
            }
        )
    return jsonify({"requests": requests_list}), 200


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


## TASK POSTINGS ##
@tasks_bp.route("/tasks/postings/all", methods=["GET"])
def get_all_postings():
    """
    /tasks/postings/all - GET
    """
    task_postings = TaskPosting.query.all()
    output = []
    for task_posting in task_postings:
        task_id = task_posting.task
        task = Task.query.filter_by(id=task_id).first()
        output.append(
            {
                "id": task_posting.id,
                "name": task.name,
                "reward": task.reward,
                "start_time": task.start_time,
                "end_time": task.end_time,
                "recurrence_interval": task.recurrence_interval,
                "description": task.description,
                "created_by": task.created_by,
                "status": task_posting.status,
                "user_limit": task_posting.user_limit,
            }
        )


@tasks_bp.route("/tasks/postings", methods=["POST"])
@user_logged_in(is_admin=True)
def create_task_posting():
    """
    /tasks/postings - POST
    Request: { "task_id": str, "user_limit": int }
    """
    data = request.get_json() or {}
    task_id = data.get("task_id")
    task = Task.query.filter_by(id=task_id).first()
    if not task:
        return jsonify({"success": False, "message": "Invalid task id"}), 400

    new_task_posting = TaskPosting(
        id=uuid.uuid4().hex,
        task=task_id,
        user_limit=data.get("user_limit"),
    )
    new_log_item = Log(
        id=uuid.uuid4().hex,
        uid=current_user.uid,
        cat="TASK",
        timestamp=db.func.current_timestamp(),
        description=f"Admin {current_user.uid} created task posting {new_task_posting.id}",
    )
    db.session.add(new_task_posting)
    db.session.add(new_log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task posting created"}), 200


@tasks_bp.route("/tasks/postings/<string:posting_id>/update", methods=["PATCH"])
@user_logged_in(is_admin=True)
def update_task_posting(posting_id):
    """
    /tasks/postings/<posting_id>/update - PATCH
    Request: { "task_posting": {...} }
    """
    data = request.get_json() or {}
    task_posting_data = data.get("task_posting", {})
    if not posting_id:
        return jsonify({"success": False, "message": "Task posting ID required"}), 400

    task_posting = TaskPosting.query.filter_by(id=posting_id).first()
    if not task_posting:
        return jsonify({"success": False, "message": "Task posting not found"}), 404

    diff = generate_update_diff(task_posting, task_posting_data)

    protected_update(task_posting, "user_limit", task_posting_data, admin_only=True)
    protected_update(task_posting, "is_open", task_posting_data, admin_only=True)
    log_item = Log(
        id=uuid.uuid4().hex,
        uid=current_user.uid,
        cat="TASK",
        timestamp=db.func.current_timestamp(),
        description=f"Admin {current_user.uid} made the following changes: {diff} on task posting {posting_id}",
    )
    db.session.add(log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task posting updated"}), 200


@tasks_bp.route("/tasks/postings/<string:posting_id>/delete", methods=["DELETE"])
@user_logged_in(is_admin=True)
def delete_task_posting(posting_id):
    """
    /tasks/postings/<posting_id>/delete - DELETE
    Request: {}
    """
    data = request.get_json() or {}
    task_posting = TaskPosting.query.filter_by(id=posting_id).first()
    if not task_posting:
        return jsonify({"success": False, "message": "Task posting not found"}), 404

    db.session.delete(task_posting)
    log_item = Log(
        id=uuid.uuid4().hex,
        uid=current_user.uid,
        cat="TASK",
        timestamp=db.func.current_timestamp(),
        description=f"Admin {current_user.uid} deleted task posting {posting_id}",
    )
    db.session.add(log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task posting deleted"}), 200


## Task Application #
@tasks_bp.route("/tasks/postings/<string:posting_id>/apply", methods=["POST"])
@user_logged_in()
def apply_task_posting(posting_id):
    """
    /tasks/postings/<posting_id>/apply - POST
    Request: {}
    """
    task_posting = TaskPosting.query.filter_by(id=posting_id).first()
    if not task_posting:
        return jsonify({"success": False, "message": "Task posting not found"}), 404

    new_application = TaskApplication(
        id=uuid.uuid4().hex,
        posting=posting_id,
        user=current_user.uid,
        status="PENDING",
    )
    new_log_item = Log(
        id=uuid.uuid4().hex,
        uid=current_user.uid,
        cat="TASK",
        timestamp=db.func.current_timestamp(),
        description=f"User {current_user.uid} applied for task posting {posting_id}",
    )
    db.session.add(new_application)
    db.session.add(new_log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task posting applied"}), 200


@tasks_bp.route("/tasks/applications", methods=["GET"])
def get_task_applications():
    """
    /tasks/postings/<string:posting_id>/applications - GET
    """
    task_applications = TaskApplication.query.all()
    output = []
    for ta in task_applications:
        output.append(
            {
                "id": ta.id,
                "posting": ta.posting,
                "user": ta.user,
                "status": ta.status,
                "comment": ta.comment,
            }
        )
    return jsonify({"task_postings": output}), 200


@tasks_bp.route("/tasks/applications/<string:application_id>/cancel", methods=["POST"])
@user_logged_in()
def cancel_task_application(application_id):
    """
    /tasks/applications/<application_id>/cancel - POST
    Request: {}
    """
    task_application = TaskApplication.query.filter_by(id=application_id).first()
    if not task_application:
        return jsonify({"success": False, "message": "Invalid application id"}), 400
    if task_application.status != "pending":
        return jsonify({"success": False, "message": "Application already accepted"}), 400

    if current_user.cat != "ADMIN" and current_user.uid != task_application.user:
        return jsonify({"success": False, "message": "You are not authorized to cancel this application"}), 403

    db.session.delete(task_application)
    log_item = Log(
        id=uuid.uuid4().hex,
        uid=current_user.uid,
        cat="TASK",
        timestamp=db.func.current_timestamp(),
        description=f"User {current_user.uid} canceled for task application {task_application.id}",
    )
    db.session.add(log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Application cancelled"}), 200


@tasks_bp.route("/tasks/applications/<string:application_id>/review", methods=["POST"])
@user_logged_in(is_admin=True)
def review_task_application(application_id):
    """
    /tasks/applications/<application_id>/review - POST
    Request: { "will_approve": bool, "comment": str }
    """
    data = request.get_json() or {}
    if not (will_approve := data.get("will_approve")):
        return (
            jsonify({"success": False, "message": "Please indicate either approval or rejection of the application"}),
            400,
        )

    task_application = TaskApplication.query.filter_by(id=application_id).first()
    if not task_application:
        return jsonify({"success": False, "message": "Invalid application id"}), 400

    if task_application.status != "PENDING":
        return jsonify({"success": False, "message": "Application is already reviewed"}), 400

    task_posting = TaskPosting.query.filter_by(id=task_application.posting).first()
    task = Task.query.filter_by(id=task_posting.task).first()

    if will_approve:
        user_tasks = create_user_tasks(task, task_application.user)
        db.session.add_all(user_tasks)
        task_application.status = "APPROVED"
        task_application.comment = data.get("comment")
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"Admin {current_user.uid} approved task {task.id} for user {task_application.user}",
        )
    else:
        task_application.status = "REJECTED"
        task_application.comment = data.get("comment")
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"Admin {current_user.uid} rejected task {task.id} for user {task_application.user}",
        )
    db.session.add(log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task application reviewed"}), 200


## TASK SUBMISSION ##


@tasks_bp.route("/tasks/submissions/<string:usertask_id>/submit", methods=["POST"])
@user_logged_in()
def submit_task(usertask_id):
    """
    /tasks/submissions/<usertask_id>/submit - POST
    Request: { "proof": blob }
    """
    request_data = request.get_json() or {}
    proof = request_data.get("proof")

    usertask = UserTask.query.filter_by(id=usertask_id).first()
    if not usertask:
        return jsonify({"success": False, "message": "User task not found"}), 404

    task = Task.query.filter_by(id=usertask.task).first()

    if current_user.cat != "ADMIN" and current_user.uid != usertask.uid:
        return jsonify({"success": False, "message": "You are not authorised to submit this task"}), 403

    if usertask.status != "ONGOING" or usertask.status != "CHANGES_REQUESTED":
        return jsonify({"success": False, "message": "This task cannot be submitted"}), 400

    if usertask.status == "ONGOING":
        if usertask.end_time < datetime.datetime.now():
            return jsonify({"success": False, "message": "The task deadline has passed"}), 400

        if usertask.start_time > datetime.datetime.now():
            return jsonify({"success": False, "message": "The task has not started yet"}), 400

    if task.require_proof and (proof is None or usertask.proof_of_completion is None):
        return jsonify({"success": False, "message": "Proof is required for this task"}), 400

    if task.require_review:
        usertask.status = "UNDER_REVIEW"
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"User {current_user.uid} submitted task {task.id} for review",
        )
    else:
        usertask.status = "COMPLETED"
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"User {current_user.uid} submitted task {task.id}",
        )
        current_user.credit += task.reward
    db.session.add(log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task submission successful"}), 200


@tasks_bp.route("/tasks/submissions/<string:usertask_id>/review", methods=["POST"])
@user_logged_in(is_admin=True)
def review_task_submission(usertask_id):
    """
    /tasks/submissions/<usertask_id>/review - POST
    Request: { "action": APPROVE|REQUEST_CHANGES|REJECT, "comment": str }
    """
    data = request.get_json() or {}
    if not (action := data.get("action")):
        return (
            jsonify({"success": False, "message": "Please indicate how you would like to review the task submission"}),
            400,
        )

    usertask = UserTask.query.filter_by(id=usertask_id).first()
    if not usertask:
        return jsonify({"success": False, "message": "User task not found"}), 404

    if usertask.status != "UNDER_REVIEW":
        return (
            jsonify({"success": False, "message": "This task is already completed or is not ready to be reviewed"}),
            400,
        )

    if action == "APPROVE":
        usertask.status = "COMPLETED"
        usertask.admin_comment = data.get("comment")
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"Admin {current_user.uid} approved task submission {usertask.id}",
        )
        user = User.query.filter_by(uid=usertask.uid).first()
        user.credit += usertask.task.reward
    elif action == "REQUEST_CHANGES":
        usertask.status = "CHANGES_REQUESTED"
        usertask.admin_comment = data.get("comment")
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"Admin {current_user.uid} requested changes for task submission {usertask.id}",
        )
    elif action == "REJECT":
        usertask.status = "REJECTED"
        usertask.admin_comment = data.get("comment")
        log_item = Log(
            id=uuid.uuid4().hex,
            uid=current_user.uid,
            cat="TASK",
            timestamp=db.func.current_timestamp(),
            description=f"Admin {current_user.uid} rejected task submission {usertask.id}",
        )
    else:
        return jsonify({"success": False, "message": "Action can only be APPROVE, REQUEST_CHANGES, or REJECT"}), 400
    db.session.add(log_item)
    db.session.commit()
    return jsonify({"success": True, "message": "Task submission reviewed"}), 200


## USER TASKS ##
@tasks_bp.route("/tasks/usertasks", methods=["GET"])
def get_all_usertasks():
    """
    /tasks/usertasks - GET
    Optional parameter: uid
    """
    user_id = request.args.get("uid")
    if user_id:
        usertasks = UserTask.query.filter_by(uid=user_id).all()
    else:
        usertasks = UserTask.query.all()

    usertasks_list = []
    for ut in usertasks:
        usertasks_list.append(
            {
                "id": ut.id,
                "uid": ut.uid,
                "task": ut.task,
                "status": ut.status,
                "proof_of_completion": ut.proof_of_completion,
                "admin_comment": ut.admin_comment,
            }
        )
    return jsonify({"usertasks": usertasks_list}), 200
