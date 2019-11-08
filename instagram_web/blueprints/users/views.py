
import re

from flask import Blueprint, render_template, redirect, url_for, flash, request
from werkzeug.security import generate_password_hash
from models.user import User


users_blueprint = Blueprint('users',
                            __name__,
                            template_folder='templates')


@users_blueprint.route('/new', methods=['GET'])
def new():
    return render_template('users/new.html')


@users_blueprint.route('/new', methods=['POST'])
def create():
    # if len(request.get.form('password')) < 6:
    #     flash ('Password must be at least 6 characters!')
    password = request.form.get('password')
    if re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", password):
        print("first if")
        full_name = request.form.get('full_name')
        username = request.form.get('username')
        email = request.form.get('email')
        password = generate_password_hash(password)

        user = User(full_name=full_name, username=username, email=email, password=password)

        if user.save():
            print(
                "saved"
            )
            return redirect(url_for('users.new'))
       
       
    else:
        print("not entered")
        flash ('Password must be at least 6 characters.\nPassword must contain capital letter.\nPassword must have one special character')
        return render_template('users/new.html')
   
    


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
