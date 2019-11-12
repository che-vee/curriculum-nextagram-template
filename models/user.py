import peewee as pw
import re
from werkzeug.security import generate_password_hash

from models.base_model import BaseModel
from flask_login import UserMixin


class User(UserMixin, BaseModel):
    full_name = pw.CharField()
    username = pw.CharField(unique=True)
    email = pw.CharField(unique=True)
    password = pw.CharField()

    def is_authenticated(self):
        return True
    
    def is_active(self):
        return True
    
    # server side validation for user
    def validate(self):
        duplicate_username = User.get_or_none(User.username == self.username)
        duplicate_email = User.get_or_none(User.email == self.email)

        # check if duplicate username
        if duplicate_username and not duplicate_username.id == self.id:
            self.errors.append('Username already in use')

        # check if dupliacte email
        if duplicate_email and not duplicate_email.id == self.id:
            self.errors.append('Email already in use')

        # check if password meets criteria and return hashed password
        if not re.match(r"^(?=.*[\d])(?=.*[A-Z])(?=.*[a-z])(?=.*[@#$])[\w\d@#$]{6,12}$", self.password):
            self.errors.append('Password must be at least 6 characters.\nPassword must contain capital letter.\nPassword must have one special character')
        else: 
            self.password = generate_password_hash(self.password)

    