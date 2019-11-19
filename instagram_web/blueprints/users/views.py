import re

from flask import Blueprint, render_template, redirect, url_for, flash, request
from flask_login import login_required, current_user

from models.user import User
from models.relationship import Relationship
from werkzeug.security import generate_password_hash
from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
from config import Config




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
    user = User.select().where(User.username == username).get()

    print(user.profile_image_url)

    return render_template('users/profile.html', user=user)


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

@users_blueprint.route('/<id>/new', methods=['POST'])
@login_required
def upload_profile_image(id):
    # get a file from request
    file = request.files["user_file"]
	# if no file in request
    if not file:
        flash("Please choose a file", 'danger')
        return render_template('users/edit.html')
	# if there is a file in request & is allowed type
    elif file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        output = upload_file_to_s3(file)

        if not output:
            flash(f'Unable to upload {file.filename}, please try again.', 'danger')
            return render_template('users/edit.html')

        else:
            # get current user
            user = User.update(profile_image = output).where(User.id == current_user.id)
            # save profile image link 
            user.execute()
            flash(f'Successfully uploaded {file.filename}', 'success')
            return redirect(url_for('users.show', username=current_user.username))


# follower following relationship section
@users_blueprint.route('/follow/<id>', methods=['POST'])
@login_required
def follow(id):
    fan_id = current_user.id
    idol_id = request.form.get('idol_id')
    idol = User.get_by_id(idol_id)

    follower = Relationship(fan=fan_id, idol=idol_id)
    follower.save()

    return render_template('users/profile.html')

  