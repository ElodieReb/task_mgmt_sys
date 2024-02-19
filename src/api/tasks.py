from flask import Blueprint, jsonify, abort, request
from ..models import Task, User, db

import traceback

bp = Blueprint('tasks', __name__, url_prefix='/tasks')

@bp.route('', methods=['GET'])  # GETs all tasks
def index():
    tasks = Task.query.all() 
    result = []
    for t in tasks:
        result.append(t.serialize()) 
    return jsonify(result)  

@bp.route('/<int:id>', methods=['GET']) # GETs a task's info after the id is entered
def show(id: int):
    t = Task.query.get_or_404(id, "Task not found")
    return jsonify(t.serialize())

@bp.route('', methods=['POST'])
def create():
    # req body must contain user_id and title
    if 'created_by_user' not in request.json or 'title' not in request.json or 'description' not in request.json or 'deadline' not in request.json or 'status' not in request.json:
        return abort(400)

    # user with id of user_id must exist
    u = User.query.get_or_404(request.json['created_by_user'], "User not found")

    # construct Task without assigning it to anyone initially
    t = Task(
        title=request.json['title'],
        description=request.json['description'],
        deadline=request.json['deadline'],
        status=request.json['status'],
        created_by_user=request.json['created_by_user']
    )

    try:
        db.session.add(t)  # prepare CREATE statement
        db.session.commit()  # execute CREATE statement

        # Note: Do not assign the task to the user automatically here

        return jsonify(t.serialize())
    except Exception as e:
        # Handle any exceptions, e.g., rollback changes
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>', methods=['PATCH', 'PUT'])
def update(id: int):
    t = Task.query.get_or_404(id)

    if 'title' not in request.json: # checks to make sure the title exists first
        return abort(400)
    
    if 'title' in request.json:
        t.title = request.json['title'] # updates title

    if 'description' in request.json:
        t.description = request.json['description'] # updates description

    if 'deadline' in request.json:
        t.deadline = request.json['deadline'] # updates deadline

    if 'status' in request.json:
        t.status = request.json['status'] # updates status

    try:
        db.session.commit()  # save updates to the database
        return jsonify(t.serialize())
    except:
        # something went wrong :(
        return jsonify(False)

@bp.route('/<int:id>', methods=['DELETE']) 
def delete(id: int):
    t = Task.query.get_or_404(id, "Task not found")

    try:
        db.session.delete(t)  # prepare DELETE statement
        db.session.commit()  # execute DELETE statement
        return jsonify(True)
    except Exception as e:
        # Handle any exceptions, e.g., rollback changes
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@bp.route('/<int:id>/assign_to/<int:user_id>', methods=['POST'])
def assign_task(id: int, user_id: int):
    t = Task.query.get_or_404(id, "Task not found")
    u = User.query.get_or_404(user_id, "User not found")

    # Call the assign_user method
    if not t.assign_user(u):
        return jsonify({'message': 'Task already assigned to the user'}), 400

    try:
        db.session.commit()  # Save changes to the database
        return jsonify({'message': 'Task assigned successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback changes if an exception occurs
        return jsonify({'message': f'Error assigning task: {str(e)}'}), 500

@bp.route('/<int:id>/users_assigned_task', methods=['GET']) 
def users_assigned_task(id: int):
    t = Task.query.get_or_404(id)

    # Check if there are users assigned
    if not t.assignees:
        return jsonify({'message': 'No users currently assigned to task.'})

    # Use list comprehension to serialize assigned users
    result = [user.serialize() for user in t.assignees]

    return jsonify(result)

@bp.route('/<int:id>/unassign_user/<int:user_id>', methods=['PATCH','PUT'])
def unassign_user(id: int, user_id: int):
    t = Task.query.get_or_404(id, "Task not found")
    u = User.query.get_or_404(user_id, "User not found")

    # Check if the user is assigned to the task
    if u not in t.assignees:
        return jsonify({'message': 'User is not assigned to the task'}), 400

    # Remove the user from the assignees list
    t.assignees.remove(u)

    try:
        db.session.commit()  # Save changes to the database
        return jsonify({'message': 'User unassigned successfully'}), 200
    except Exception as e:
        db.session.rollback()  # Rollback changes if an exception occurs
        return jsonify({'message': f'Error unassigning user from task: {str(e)}'}), 500