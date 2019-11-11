from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from models.user import User
from werkzeug.security import check_password_hash

sessions_blueprint = Blueprint('sessions', __name__, template_folder='templates')

@sessions_blueprint.route('/login', methods=['GET'])
def new():
    return render_template('sessions/new.html')

@sessions_blueprint.route('/login', methods=['POST'])
def create():

    # get user information from form
    username = request.form.get('username')
    password_to_check = request.form.get('password')

    # check if username exists in database
    user=User.get_or_none(User.username == username)
   

    if user:
        hashed_password = (user.password)
        if check_password_hash(hashed_password, password_to_check):
            session['user.id'] = user.id
            flash('Successfully logged in!', 'success')
            return redirect(url_for('users.new'))
        else:
            flash('Login unsuccesful. Please check username & password.')
            return render_template('sessions/new.html', username=username)
    else:
        flash('User does not exsist.')
        return render_template('sessions/new.html', username=username)
       
