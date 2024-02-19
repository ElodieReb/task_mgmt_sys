from flask_sqlalchemy import SQLAlchemy
import datetime

db = SQLAlchemy()

assignees_table = db.Table(
    'task_assignees',
    db.Column('user_id', db.Integer, db.ForeignKey('users.id'), primary_key=True),
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), primary_key=True),
    db.Column('created_at', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
)

class Task(db.Model):
    __tablename__ = 'tasks'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(256), unique=True, nullable=False)
    description = db.Column(db.Text)
    deadline = db.Column(db.Date)
    status = db.Column(db.String(50))
    created_by_user = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=True)

    created_by = db.relationship('User', back_populates='tasks_created_by_user', foreign_keys=[created_by_user], overlaps='created_by_user_rel')
    assignees = db.relationship(
        'User',
        secondary=assignees_table,
        back_populates='assigned_tasks',
        lazy='select'
    )

    @property
    def users_assigned_task(self):
        if self.assignees:
            return [user.serialize() for user in self.assignees]
        else:
            return []
        
    def assign_user(self, user):
        if user not in self.assignees:
            self.assignees.append(user)
            db.session.commit()
            return True
        else:
            return False

    def __init__(self, title, description, deadline, status, created_by_user):
        self.title = title
        self.description = description
        self.deadline = deadline
        self.status = status
        self.created_by_user = created_by_user

    def serialize(self):
        assigned_users = [user.serialize() for user in self.assignees]
        return {
            'task_id': self.id,
            'title': self.title,
            'description': self.description,
            'deadline': self.deadline,
            'status': self.status,
            'created_by_user': self.created_by_user,
            'assigned_users': assigned_users
        }

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    username = db.Column(db.String(128), unique=True, nullable=False)
    email = db.Column(db.String(128), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.datetime.utcnow, nullable=True)

    tasks_created_by_user = db.relationship('Task', back_populates='created_by', lazy=True)
    assigned_tasks = db.relationship(
        'Task',
        secondary=assignees_table,
        back_populates='assignees',
        lazy='select'
    )

    def __init__(self, username, email, password, created_at=None):
        self.username = username
        self.email = email
        self.password = password
        self.created_at = created_at or datetime.datetime.utcnow()

    def serialize(self):
        return {
            'user_id': self.id,
            'username': self.username,
            'email': self.email
        }

task_progress_table = db.Table(
    'task_logs',
    db.Column('task_id', db.Integer, db.ForeignKey('tasks.id'), nullable=False),
    db.Column('status', db.String(50), nullable=False),
    db.Column('timestamp', db.DateTime, default=datetime.datetime.utcnow, nullable=False)
)
