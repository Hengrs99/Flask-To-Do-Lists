from flask import Blueprint, request, jsonify, flash, redirect, url_for
from flask_login import current_user
from . import db
from .models import List, Task
import json, os

api = Blueprint('api', __name__)

# API

def get_current_list_id():
    """
    reads id of currently used list from .current_list_id.txt
    :return: id of current list
    """
    path = f'{os.path.dirname(os.path.realpath(__file__))}\\current_list_id.txt'
    with open(path, 'r') as f:
        current_list_id = f.readline()
        
    return current_list_id

def set_current_list_id(list_id):
    """
    saves id of currently used list to .current_list_id.txt
    :param list_id: int
    :return: None
    """
    list_id = list_id
    path = f'{os.path.dirname(os.path.realpath(__file__))}\\current_list_id.txt'
    with open(path, 'w') as f:
        f.write(str(list_id))

@api.route('/add_task', methods=['POST'])
def add_task():
    """
    adds new task specified by user to database
    :exception: POST
    :return: an empty json dobject
    """
    list_id = get_current_list_id()
    list = List.query.get(list_id)
    task_data = json.loads(request.data)
    task_text = task_data['taskText']

    if len(task_text) < 2:
        flash('Item description is too short!', category='error')
    else:
        new_task = Task(text=task_text, finished=False, list_id=list_id)
        db.session.add(new_task)
        db.session.commit()
    
    return jsonify({})

@api.route('/get_list_id', methods=['POST'])
def get_list_id():
    """
    gets id of currently used list by reading info sent by frontend
    :exception: POST
    :return: an empty json object
    """
    list_data = json.loads(request.data)
    list_id = list_data['listId']
    list = List.query.get(list_id)

    if list:    
        if list.user_id == current_user.id:
            set_current_list_id(list.id)
    
    return jsonify({})

@api.route('/update_task_state', methods=['POST'])
def update_task_state():
    """
    changes state of currently modified task based on id sent by frontend
    :exception: POST
    :return: an empty json object
    """
    task_data = json.loads(request.data)
    task_id = task_data['taskId']
    task_to_update = Task.query.get(task_id)

    if task_to_update:    
        task_to_update.finished = not task_to_update.finished
        db.session.commit()
    
    return jsonify({})

@api.route('/delete_list', methods=['POST'])
def delete_list():
    """
    deletes specified list using id sent by frontend
    :exception: POST
    :return: an empty json object
    """
    list_data = json.loads(request.data)
    list_id = list_data['listId']
    list_to_delete = List.query.get(list_id)

    if list_to_delete:
        if list_to_delete.user_id == current_user.id:
            db.session.delete(list_to_delete)
            db.session.commit()

    return jsonify({})

@api.route('/delete_task', methods=['POST'])
def delete_task():
    """
    deletes specified task using id sent by frontend
    :exception: POST
    :return: an empty json object
    """
    task_data = json.loads(request.data)
    task_id = task_data['taskId']
    task_to_delete = Task.query.get(task_id)

    if task_to_delete:
        db.session.delete(task_to_delete)
        db.session.commit()

    return jsonify({})

@api.route('/return_to_lists')
def return_to_lists():
    """
    redirects user to main page
    :return: None
    """
    flash('List Saved!')
    return redirect(url_for('views.user_lists'))