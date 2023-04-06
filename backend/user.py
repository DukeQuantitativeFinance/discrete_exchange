from flask_login import UserMixin

from .database import database

# define user class
# see: https://stackoverflow.com/questions/54992412/flask-login-usermixin-class-with-a-mongodb
class User(UserMixin):
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
    def save_to_database(self):
        user = {'username': self.username, 'password': self.password}
        database.users.insert_one(user)