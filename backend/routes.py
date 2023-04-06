import os
from flask import Blueprint, request
from flask_login import login_user

from .user import User
from .app_discrete_exchange.server import Server

main_routes = Blueprint('main_routes', __name__)
@main_routes.route('/', methods = ['GET'])
def home():
    return '<h1></h1>'

# see: https://pythonbasics.org/flask-login/
@main_routes.route('/signup', methods = ['GET', 'POST'])
def signup():  
    username = request.form.get('username')
    password = request.form.get('password')
    print("username: ", username)
    print("password: ", password)
    
    # create User object and save to database
    user = User(username, password)
    user.save_to_database()
    return '<h1></h1>'

@main_routes.route('/login', methods = ['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    

# DISCRETE EXCHANGE ROUTES
servers = {} # map of game ids to server objects
user_to_game = {} # map of user ids to game ids

discrete_exchange_routes = Blueprint('discrete_exchange_routes', __name__)

@discrete_exchange_routes.route('/discrete', methods = ['GET'])
def home_screen():
    if request.method == 'GET':
        return '<h1>Welcome!</h1>'

# route for user to host a lobby        
@discrete_exchange_routes.route('/discrete/start', methods = ['POST'])
def start_game():
    global servers, user_to_game
    
    if request.method == 'POST':
        # start new server
        new_server = Server()
        game_id = 'test_game_id'
        servers[game_id] = new_server
        
        # add host player to server?        

# route for user to join a lobby
@discrete_exchange_routes.route('/discrete/join', methods = ['POST'])
def join_game():
    global user_to_game
    
    if (request.method == 'POST'):
        # get user and game ids from request
        user_id = request.form.get('userId')
        game_id = request.form.get('gameId')
        
        game_server = servers[game_id] # get server object
        game_server.add_user(user_id) # add user to server
        user_to_game[user_id] = game_id # map user id to game id
        
        
# route for user to submit file
@discrete_exchange_routes.route('/discrete/submit', methods = ['POST'])
def submit_trader():
    global servers
    
    if request.method == 'POST':
        print('submission received')
        file = request.files['file']
        filename = file.filename
        file.save(os.path.join(app.config['UPLOAD_DEST'], filename))
        
        # get user id and game id, add player to game
        user_id = request.form.get('userId')
        game_id = user_to_game[user_id]
        game_server = servers[game_id]
        game_server.add_submission(user_id, filename)
        
    return '<h1></h1>'