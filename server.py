from pathlib import Path
import importlib
import os

from trader import *
from exchange import *

class Server: 
    def __init__(self):
        self.user_ids = [] # user ids of all players
        self.id_to_filename = {} # map of user id to filename
        self.id_to_trader = {} # map of user id to trader object
        self.traders = [] # list of trader objects
        self.exchange = None
        
    def add_player(self, id, filename):
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
            
    # def import_traders(self, dirname):
    #     # loop through modules in directory specified by pathname
    #     for module_name in Path(dirname).iterdir():
    #         if module_name.suffix == '.py' and not (str(module_name) == f'{dirname}/__init__.py'):
    #             # import trader class from module and create object of trader class
    #             module_name_short = str(module_name)[18:-3]
    #             module = importlib.import_module(f'{dirname}.{module_name_short}')
    #             trader_class = getattr(module, module_name_short)
    #             trader_instance = trader_class('name')
    #             self.traders.append(trader_instance)
    
    def begin_game(self, rounds):
        # run game
        self.exchange = Exchange(['test'], *self.traders)
        self.exchange.run_game(rounds)
        
def test_server():
    s = Server()
    s.add_player('boring', 'BoringTrader.py')
    s.add_player('dumb', 'DumbTrader.py')
    s.import_all_traders()
    print(s.id_to_filename)
    
test_server()