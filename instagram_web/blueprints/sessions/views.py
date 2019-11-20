from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_user, current_user, logout_user, login_required
from models.user import User
from werkzeug.security import check_password_hash
from instagram_web.util.google_oauth import oauth

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
            # session['user.id'] = user.id

            login_user(user)
            flash('Successfully logged in!', 'success')
            return redirect(url_for('users.index'))
        else:
            
            flash('Login unsuccesful. Please check username & password.', 'danger')
            return render_template('sessions/new.html', username=username)
    else:
        flash('User does not exsist.', 'danger')
        return render_template('sessions/new.html', username=username)

@sessions_blueprint.route('/login/google', methods=['GET'])
def google_login():
    redirect_uri = url_for('sessions.authorize_google', _external=True)
    return oauth.google.authorize_redirect(redirect_uri)

@sessions_blueprint.route('/authorize/google', methods=['GET'])
def authorize_google():
    token = oauth.google.authorize_access_token()

    if not token:
        flash('Oops, something went wrong, try again!', 'danger')
        return redirect (url_for('sessions.new'))

    response = oauth.google.get('https://www.googleapis.com/oauth2/v2/userinfo')
    email = response.json()['email']

    user = User.get_or_none(User.email == email)

    if not user:
            flash('User does not exist. Please sign-up here', 'danger')
            return render_template('users/new.html')
    
    flash('Welcome back!', 'success')
    login_user(user)
    return redirect(url_for('users.show'))

@sessions_blueprint.route('/logout', methods=['GET'])
@login_required
def destroy():
    user = current_user
    logout_user()
    return redirect(url_for('sessions.new'))
       
