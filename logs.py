# logs.py
import uuid
from flask import Blueprint, jsonify
from models import db, Log

logs_bp = Blueprint('logs', __name__)

@logs_bp.route("/logs/all", methods=["GET"])
def get_all_logs():
    """
    /logs/all - GET
    Returns all logs in the system.
    """
    logs = Log.query.all()

    # Convert logs to simple dict
    logs_data = [
        {
            "id": log.id,
            "cat": log.cat,
            "uid": log.uid,
            "timestamp": log.timestamp,
            "description": log.description,
        }
        for log in logs
    ]

    return jsonify({"success": True, "logs": logs_data}), 200
