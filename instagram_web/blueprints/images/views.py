from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user

from werkzeug.utils import secure_filename
from instagram_web.util.helpers import upload_file_to_s3, allowed_file
from config import Config
from models.user import User
from models.image import Image

images_blueprint = Blueprint('images', __name__, template_folder='templates')

@images_blueprint.route('/new', methods=['GET'])
@login_required
def new():
    return render_template('images/new.html')

@images_blueprint.route('/<id>/new', methods=['POST'])
@login_required
def upload_image(id):
    # get a file from request
    file = request.files["image"]
	# if no file in request
    if not file:
        flash("Please choose a file", 'danger')
        return render_template('images/new.html')
	# if there is a file in request & is allowed type
    elif file and allowed_file(file.filename):
        file.filename = secure_filename(file.filename)
        
        output = upload_file_to_s3(file)

        if not output:
            flash(f'Unable to upload {file.filename}, please try again.', 'danger')
            return render_template('images/new.html')

        else:
            user = User.get_by_id(current_user.id)
            image = Image(filename=output, user=user)
            image.save()
            flash(f'Successfully uploaded {file.filename}', 'success')
            return redirect(url_for('images.new'))
  

@images_blueprint.route('/<id>', methods=['GET'])
@login_required
def show(id):
    user = User[current_user.id]
    return render_template('users/profile.html', user=user)
