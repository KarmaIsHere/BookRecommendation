from flask_login import UserMixin
from extensions import login_manager

class User(UserMixin):
    def __init__(self, username):
        self.id = username

    def get_username(self):
        return self.id

@login_manager.user_loader
def load_user(username):
    return User(username)
