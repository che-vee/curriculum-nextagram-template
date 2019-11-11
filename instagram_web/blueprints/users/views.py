import re

from flask import Blueprint, render_template, redirect, url_for, flash, request
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
def edit(id):
    pass


@users_blueprint.route('/<id>', methods=['POST'])
def update(id):
    pass
