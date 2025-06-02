from flask_login import UserMixin
from extensions import login_manager
import requests
import os

SPRING_API_BASE_URL = os.getenv('SPRING_API_BASE_URL', 'http://localhost:8080')

class User(UserMixin):
    def __init__(self, username, is_admin=False):
        self.id = username
        self.is_admin = is_admin

    def get_username(self):
        return self.id

@login_manager.user_loader
def load_user(username):
    try:
        response = requests.get(f"{SPRING_API_BASE_URL}/api/user/getUsername/{username}")
        response.raise_for_status()
        user_data = response.json()

        is_admin_status = user_data.get('admin', False)

        return User(username, is_admin=is_admin_status)
    except requests.RequestException as e:
        print(f"Error loading user {username} from backend: {e}")
        return None