from flask import Blueprint, jsonify, make_response
from models.user import User

users_api_blueprint = Blueprint('users_api',
                             __name__,
                             template_folder='templates')

@users_api_blueprint.route('/', methods=['GET'])
def index():
    users = User.select()

    user_list=[]
    for user in users:
        user_list.append({
          'id': user.id,
          'full_name': user.full_name,
          'username': user.username,
          'profileImage': user.profile_image_url   
        })
   
    return jsonify(user_list),200
    
