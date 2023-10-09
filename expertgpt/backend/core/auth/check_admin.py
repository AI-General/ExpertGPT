import os
from models.users import User

def check_admin(user:User):
    admin_email = os.getenv("ADMIN_EMAIL")
    return user.email == admin_email