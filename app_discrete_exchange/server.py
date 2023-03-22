from pathlib import Path
import importlib
import os

from .trader import *
from .exchange import *

class Server: 
    def __init__(self):
        self.user_ids = [] # user ids of all players
        self.id_to_filename = {} # map of user id to filename
        self.id_to_trader = {} # map of user id to trader object
        self.traders = [] # list of trader objects
        self.exchange = None
        self.allow_submission = True
    
    def add_user(self, id):
        self.user_ids.append(id)
    
    def add_submission(self, id, filename):
        if self.allow_submission:
            self.id_to_filename[id] = filename
                
    def import_individual_trader(self, id, dirname, filename):
        module_name = filename[:-3]
        module = importlib.import_module(f'{dirname}.{module_name}')
        trader_class = getattr(module, module_name)
        trader_instance = trader_class(id)
        self.traders.append(trader_instance)
        self.id_to_trader[id] = trader_instance
        
    def import_all_traders(self):
        for id in self.id_to_filename:
            self.import_individual_trader(id, 'submitted_traders', self.id_to_filename[id]) 
    
    def begin_game(self, rounds):
        # run game
        self.exchange = Exchange(['test'], *self.traders)
        self.exchange.run_game(rounds)