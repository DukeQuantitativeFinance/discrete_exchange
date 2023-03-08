from pathlib import Path
import importlib

from trader import *
from exchange import *

class Server: 
    def __init__(self):
        self.user_ids = [] # unique ids of all players
        self.id_to_trader = {} # map of unique id to trader object
        self.traders = [] # tuple of trader objects
        self.exchange = None
        
    def import_traders(self, pathname):
        # loop through modules in directory specified by pathname
        for module_name in Path(pathname).iterdir():
            if module_name.suffix == '.py' and not (str(module_name) == f'{pathname}/__init__.py'):
                # import trader class from module and create object of trader class
                module_name_short = str(module_name)[18:-3]
                module = importlib.import_module(f'{pathname}.{module_name_short}')
                trader_class = getattr(module, module_name_short)
                trader_instance = trader_class('name')
                self.traders.append(trader_instance)  
    
    def begin_game(self, rounds):
        # run game
        self.exchange = Exchange(["test"], *self.traders)
        self.exchange.run_game(rounds)
        
test_server = Server()
test_server.import_traders('submitted_traders')
test_server.begin_game(100)