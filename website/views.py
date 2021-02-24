from flask import Blueprint, render_template, request, redirect, url_for, flash, jsonify
from flask_login import login_required, current_user
from . import db
from .models import List, Task
from .api import get_current_list_id, set_current_list_id
import json

views = Blueprint('views', __name__)

def update_lists_states():
    lists = List.query.all()
    for list in lists:
        finished_tasks = 0
        for task in list.tasks:
            if task.finished: finished_tasks += 1
        if finished_tasks == len(list.tasks):
            list.finished = True
            db.session.commit()
        else:
            list.finished = False
            db.session.commit()

@views.route('/', methods=['GET', 'POST'])
@login_required
def user_lists():
    if request.method == "POST":
        list_id = get_current_list_id()
        return redirect(url_for('.open_list', user=current_user, list_id=list_id))
    
    update_lists_states()
    return render_template("user_lists.html", user=current_user)

@views.route('/add_list', methods=['GET', 'POST'])
def add_list():
    if request.method == 'POST':
        list_description = request.form.get('listDescription')
        list_name = request.form.get('listName')

        if len(list_name) < 2:
            flash('List name is too short!', category='error')
            return render_template("add_list.html", user=current_user)

        else:
            new_list = List(name=list_name, description=list_description, user_id=current_user.id, finished=False)
            db.session.add(new_list)
            db.session.commit()
            set_current_list_id(new_list.id)
            return redirect(url_for('.open_list'))
        
    return render_template("add_list.html", user=current_user)

@views.route('/open_list')
def open_list():
    list_id = get_current_list_id()
    list_to_open = List.query.get(list_id)
    list_tasks = list_to_open.tasks

    amount_of_tasks = len(list_tasks)
    finished_tasks = 0
    for task in list_tasks:
        if task.finished: finished_tasks += 1

    if amount_of_tasks != 0:
        progress_percent = int(finished_tasks / amount_of_tasks * 100)
        progress_text = f"{progress_percent}% Finished"
    else:
        progress_percent = 0
        progress_text = "No Tasks"

    return render_template("list.html", user=current_user, list=list_to_open, progress_percent=progress_percent, progress_text=progress_text)
