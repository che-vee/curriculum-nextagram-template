import re

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user
from models.user import User
from werkzeug.security import generate_password_hash



users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new', methods=['POST'])
def create():
    
    # get user information from form
    full_name = request.form.get('full_name')
    username = request.form.get('username')
    email = request.form.get('email')
    password = request.form.get('password')

    # store user information in database
    user = User(full_name=full_name, username=username, email=email, password=password)

    if user.save():
        return redirect(url_for('users.new'))
    else:
        for error in user.errors:
            flash(error,'danger')
        return render_template('users/new.html', full_name=full_name, username=username, email=email)
   
    

@users_blueprint.route('/<username>', methods=["GET"])
def show(username):
    pass


@users_blueprint.route('/', methods=["GET"])
def index():
    return "USERS"


@users_blueprint.route('/<id>/edit', methods=['GET'])
@login_required
def edit(id):
    user = User[id]
    if current_user == user:
        return render_template('users/edit.html', user=user)
    # else: 
    #     return render_template('')- error message
    


@users_blueprint.route('/<id>', methods=['POST'])
@login_required
def update(id):
    user = User[id]
    if current_user == user:
        user.full_name = request.form.get('full_name')
        user.username = request.form.get('username')
        user.email = request.form.get('email')
        user.password = request.form.get('password')
        # check hash
        # if true
        
        print ('updated')
        if user.save():
            flash("Successfully updated", 'success')
            return redirect(url_for('users.edit', id=id))
        else:
            flash(user.errors)
            # flash("Unable to update profile", 'danger')
            return render_template('users/edit.html', user=user)

  