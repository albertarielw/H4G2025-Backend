# models.py
from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'users'
    uid = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    cat = db.Column(db.String(50), nullable=False)  # e.g. 'USER' or 'ADMIN'
    email = db.Column(db.String(255), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    credit = db.Column(db.Numeric(10, 2), default=0.00)
    is_active = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<User {self.uid} {self.email}>"


class Item(db.Model):
    __tablename__ = 'items'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    image = db.Column(db.Text)
    stock = db.Column(db.Integer, nullable=False)
    price = db.Column(db.Integer, nullable=False)
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Item {self.id} {self.name}>"


class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    created_by = db.Column(db.String(36), db.ForeignKey("users.uid"), nullable=False)
    reward = db.Column(db.Numeric(10, 2), default=0.00)
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    recurrence_interval = db.Column(db.Integer)  # e.g. 1 for daily, 7 for weekly
    description = db.Column(db.Text)
    require_review = db.Column(db.Boolean, default=False)
    require_proof = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f"<Task {self.id} {self.name}>"


class TaskPosting(db.Model):
    __tablename__ = "task_postings"
    id = db.Column(db.String(36), primary_key=True)
    task = db.Column(db.String(36), db.ForeignKey("tasks.id"), nullable=False)
    user_limit = db.Column(db.Integer, default=0)
    is_open = db.Column(db.Boolean, default=True)

    def __repr__(self):
        return f"<TaskPosting {self.id} {self.name}>"


class TaskApplication(db.Model):
    __tablename__ = "task_applications"
    id = db.Column(db.String(36), primary_key=True)
    posting = db.Column(db.String(36), db.ForeignKey("task_postings.id"), nullable=False)
    applicant = db.Column(db.String(36), db.ForeignKey("users.uid"), nullable=False)
    status = db.Column(db.String(50), nullable=False)
    comment = db.Column(db.Text)

    def __repr__(self):
        return f"<TaskApplication {self.id} status={self.status}>"


class TaskRequest(db.Model):
    __tablename__ = "task_requests"
    id = db.Column(db.String(36), primary_key=True)
    created_by = db.Column(db.String(36), db.ForeignKey("users.uid"), nullable=False)
    name = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    reward = db.Column(db.Numeric(10, 2), default=0.00)
    status = db.Column(db.String(50), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    recurrence_interval = db.Column(db.Integer)  # e.g. 1 for daily, 7 for weekly

    def __repr__(self):
        return f"<TaskRequest {self.id} status={self.status}>"


class UserTask(db.Model):
    __tablename__ = "usertasks"
    id = db.Column(db.String(36), primary_key=True)
    uid = db.Column(db.String(36), db.ForeignKey('users.uid'), nullable=False)
    task = db.Column(db.String(36), db.ForeignKey('tasks.id'), nullable=False)
    start_time = db.Column(db.DateTime(timezone=True))
    end_time = db.Column(db.DateTime(timezone=True))
    status = db.Column(db.String(50), nullable=False)  # e.g. 'APPLIED', etc.
    proof_of_completion = db.Column(db.LargeBinary)
    admin_comment = db.Column(db.Text)

    def __repr__(self):
        return f"<UserTask {self.id} uid={self.uid} task={self.task}>"


class Transaction(db.Model):
    __tablename__ = 'transactions'
    id = db.Column(db.String(36), primary_key=True)
    item = db.Column(db.String(36), db.ForeignKey('items.id'), nullable=False)
    uid = db.Column(db.String(36), db.ForeignKey('users.uid'), nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    status = db.Column(db.String(50), nullable=False)

    def __repr__(self):
        return f"<Transaction {self.id} item={self.item} uid={self.uid}>"


class ItemRequest(db.Model):
    __tablename__ = 'itemrequests'
    id = db.Column(db.String(36), primary_key=True)
    requested_by = db.Column(db.String(36), db.ForeignKey('users.uid'), nullable=False)
    description = db.Column(db.Text, nullable=False)

    def __repr__(self):
        return f"<ItemRequest {self.id} requested_by={self.requested_by}>"


class Log(db.Model):
    __tablename__ = 'logs'
    id = db.Column(db.String(36), primary_key=True)
    cat = db.Column(db.String(50), nullable=False)  # e.g. 'USER', 'TRANSACTION', ...
    uid = db.Column(db.String(36))
    timestamp = db.Column(db.DateTime(timezone=True), default=db.func.current_timestamp())
    description = db.Column(db.Text)

    def __repr__(self):
        return f"<Log {self.id} cat={self.cat}>"
