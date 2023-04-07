from pathlib import Path
import importlib
import os

from .trader import *
from .exchange import *

class Server: 
    def __init__(self):
        self.user_ids = [] # user ids of all players
        self.id_to_filename = {} # map of user id to filename
        self.id_to_class = {} # map of user id to trader class
        self.id_to_trader = {} # map of user id to trader instance
        self.traders = [] # list of trader instances
        # self.classes = [] # list of trader classes
        self.exchange = None
        self.allow_submission = True
        self.id_to_pnl = {}
    
    def add_user(self, id):
        print("added user: ", id)
        self.user_ids.append(id)
    
    def add_submission(self, id, filename):
        if self.allow_submission:
            print("added submission to user: ", id)
            self.id_to_filename[id] = filename
                
    def import_individual_trader(self, id, filename):
        print("import id: ", id, "dirname:", "filename:", filename)
        module_name = filename[:-3]
        print("module name: ", module_name)
        # module = importlib.import_module(f'{os.path.dirname(__file__)}.backend.{dirname}.{module_name}')
        module = importlib.import_module(f'.{module_name}', package=__package__)
        
        class_name = 'Trader'
        trader_class = getattr(module, class_name)
        
        # trader_instance = trader_class(id)
        # print("created trader instance")
        # self.traders.append(trader_instance)
        # self.id_to_trader[id] = trader_instance
        self.id_to_class[id] = trader_class
        print("trader class imported successfully")        
        
    def import_all_traders(self):
        for id in self.id_to_filename:
            self.import_individual_trader(id, '', self.id_to_filename[id]) 
    
    def initialize_traders(self):
        for id in self.id_to_class:
            # create instance of trader
            trader_class = self.id_to_class[id]
            trader_instance = trader_class(id)
            self.traders.append(trader_instance)
            self.id_to_trader[id] = trader_instance # attach user id to trader instance
      
    # reset trader objects between games to allow for existing users to submit new traders    
    def reset_trader_instances(self):
        self.traders = []
        self.id_to_trader = {}
    
    def begin_game(self, rounds):
        # run game
        self.initialize_traders()
        self.exchange = Exchange(['test'], *self.traders)
        self.exchange.run_game(rounds)
        
    def begin_round_robin(self, rounds):
        # run games for every pair of traders
        self.initialize_traders()
        for t1 in range(0, len(self.user_ids)):
            for t2 in range(t1 + 1, len(self.user_ids)):
                print("id1: ", t1)
                print("id2: ", t2)
                id1 = self.user_ids[t1]
                id2 = self.user_ids[t2]
                trader1 = self.id_to_trader[id1]
                trader2 = self.id_to_trader[id2]
                round_robin_exchange = Exchange(['test'], trader1, trader2)
                round_robin_exchange.run_game(rounds)
                trader1_pnl = round_robin_exchange.get_pnl(trader1)
                trader2_pnl = round_robin_exchange.get_pnl(trader2)
                
                if id1 in self.id_to_pnl:
                    self.id_to_pnl[id1] = self.id_to_pnl[id1] + trader1_pnl
                else:
                    self.id_to_pnl[id1] = trader1_pnl
                
                if id2 in self.id_to_pnl:
                    self.id_to_pnl[id2] = self.id_to_pnl[id2] + trader2_pnl
                else:
                    self.id_to_pnl[id2] = trader2_pnl
                                