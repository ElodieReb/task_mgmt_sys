from flask import Blueprint, jsonify, abort, request
from ..models import User, db

import hashlib
import secrets

def scramble(password: str):
    """Hash and salt the given password"""
    salt = secrets.token_hex(16)
    return hashlib.sha512((password + salt).encode('utf-8')).hexdigest()

bp = Blueprint('users', __name__, url_prefix='/users')

@bp.route('', methods=['GET'])  # decorator takes path and list of HTTP verbs
def index():
    users = User.query.all()  # ORM performs SELECT query
    result = []
    for u in users:
        result.append(u.serialize())  # build list of Tweets as dictionaries
    return jsonify(result)  # return JSON response

@bp.route('/<int:id>', methods=['GET'])
def show(id: int):
    u = User.query.get_or_404(id, "User not found")
    return jsonify(u.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain username and password
    if 'username' not in request.json or 'password' not in request.json or 'email' not in request.json:
        return abort(400)

    # construct User
    u = User(
        username=request.json['username'],
        email=request.json['email'],
        password=scramble(request.json['password'])
    )

    db.session.add(u)  # prepare CREATE statement
    db.session.commit()  # execute CREATE statement

    return jsonify(u.serialize())

@bp.route('/<int:id>', methods=['DELETE']) 
def delete(id: int):                        
    u = User.query.get_or_404(id, "User not found")
    
    try:
        db.session.delete(u)
        db.session.commit()
        return jsonify(True)
    except Exception as e:
        # Handle the exception (e.g., log it)
        print(str(e))
        db.session.rollback()  # Rollback the changes in case of an error
        return jsonify(False)

@bp.route('/<int:id>', methods=['PATCH', 'PUT']) # updates username, email, or password (no req. for username or pwd)
def update(id: int):
    u = User.query.get_or_404(id)

    if 'username' not in request.json and 'password' not in request.json or 'email' not in request.json:
        return abort(400)
    
    if 'username' in request.json:
        u.username = request.json['username']

    if 'password' in request.json:
        u.password = scramble(request.json['password'])

    if 'email' in request.json:
        u.email = request.json['email']

    try:
        db.session.commit()  # save updates to the database
        return jsonify(u.serialize())
    except:
        # something went wrong :(
        return jsonify(False)

@bp.route('/<int:id>/tasks_assigned', methods=['GET']) 
def tasks_assigned(id: int):
    u = User.query.get_or_404(id)
    result = [task.serialize() for task in u.assigned_tasks]
    
    # Check if there are tasks assigned
    if not result:
        return jsonify({'message': 'No tasks assigned to the user.'}), 200

    return jsonify(result)
