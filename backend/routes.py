import os
from flask import Blueprint, request, jsonify
from flask_login import login_user
import shutil
from flask_cors import CORS, cross_origin

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
test_server = Server()
servers = {'test_game': test_server} # map of game ids to server objects
user_to_game = {} # map of user ids to game ids

discrete_exchange_routes = Blueprint('discrete_exchange_routes', __name__)

@discrete_exchange_routes.route('/discrete', methods = ['GET'])
def home_screen():
    if request.method == 'GET':
        return '<h1>Welcome to the discrete exchange!</h1>'

# route for user to host a lobby        
# @discrete_exchange_routes.route('/discrete/start', methods = ['POST'])
# def start_game():
#     global servers, user_to_game
    
#     if request.method == 'POST':
#         if request.form.get('code') == 'admin':
#             print('game started')
#             # start new server
#             new_server = Server()
#             game_id = 'test_game_id'
#             servers[game_id] = new_server
        
#             # add host player to server?        

# route for user to join a lobby
# @discrete_exchange_routes.route('/discrete/join', methods = ['POST'])
# def join_game():
#     global user_to_game
    
#     if (request.method == 'POST'):
#         # get user and game ids from request
#         user_id = request.form.get('userId')
#         game_id = request.form.get('gameId')
        
#         game_server = servers[game_id] # get server object
#         game_server.add_user(user_id) # add user to server
#         user_to_game[user_id] = game_id # map user id to game id
        
        
# route for user to submit file
@discrete_exchange_routes.route('/discrete/submit', methods = ['POST'])
@cross_origin()
def submit_trader():
    global servers
    
    if request.method == 'POST':
        print('submission received')
        user_id = request.form.get('userId')
        game_id = request.form.get('gameId')
        
        print("user id: ", user_id)
        print("game id: ", game_id)
        
        if (game_id in servers):
            game_server = servers[game_id]
            game_server.add_user(user_id)
            user_to_game[user_id] = game_id
            file = request.files['file[]']
            filename = file.filename
            print("filename: ", filename)
            
            # save file to this directory and also save a copy to submitted_traders directory
            filepath = os.path.join(os.path.dirname(__file__) + '/app_discrete_exchange', filename)
            file.save(filepath)
            shutil.copyfile(filepath, f'{os.path.dirname(__file__)}/submitted_traders/{filename}')

            # attach filename to user id
            game_server.add_submission(user_id, filename)
            game_server.import_individual_trader(user_id, filename)
            
            # game_server.initialize_traders()
            # game_server.begin_game(100)
            # print(game_server.exchange.get_pnl(game_server.id_to_trader['test_user']))
    return '<h1></h1>'
        

@discrete_exchange_routes.route('/discrete/start', methods = ['POST'])
@cross_origin()
def start_game():
    global servers
    
    if request.method == 'POST':
        game_id = request.form.get('gameId')
        print("start game request received with game id: ", game_id)
        
        if (game_id in servers):
            print("game exists, starting next round")
            game_server = servers[game_id]
            print(game_server.user_ids)
            game_server.reset_trader_instances()
            game_server.begin_round_robin(100)
    
    return '<h1></h1>'

@discrete_exchange_routes.route('/discrete/results', methods = ['POST'])
@cross_origin()
def get_results():
    global servers
    
    if request.method == 'POST':
        game_id = request.form.get('gameId')
        user_id = request.form.get('userId')
        print("get results request received with id: ", user_id)
        
        if (game_id in servers):
            game_server = servers[game_id]
            print(game_server.id_to_pnl)
            pnl = game_server.id_to_pnl[user_id]
            print(pnl)
            response = {'pnl': pnl}
            return jsonify(response)
            
    return '<h1></h1>'