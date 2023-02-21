from dataclasses import dataclass
from typing import *
from copy import deepcopy
import random
import heapq

from trader import BaseTrader

MAX_PRICE = 100
MIN_PRICE = 0
N_LEVELS = MAX_PRICE - MIN_PRICE + 1
# limit max order size, max&min price
# price time priority: first order = first paid, delete newest to oldest
# deletion orders
# limit orders


@dataclass
class Order:
    price: int
    round: int
    owner: str
    size: int
    buy = True

    def __lt__(self, other: Self):  # price time priority
        return self.price < other.price or (self.price == other.price and self.round < other.round)

    def __eq__(self, other):
        return self.price == other.price and self.round == other.round

    def __repr__(self):
        if self.buy:
            return f"{self.owner} buy {self.size}x${self.price} (round {self.round})"
        else:
            return f"{self.owner} sell {self.size}x${self.price} (round {self.round})"

class BuyOrder(Order):
    buy = True

class SellOrder(Order):
    buy = False




class OrderBook:
    def __init__(self, product):
        self.product = product
        self.bids = []  # buy prices
        self.offers = []  # sell prices

    def buy(self, order):
        pass

    def sell(self, order):
        pass

    def add_new_quote(self, quote):
        pass

    def create_copy(self):
        pass


class Exchange:
    def __init__(self, products, *traders: BaseTrader, seed=None):
        # TODO: set min and max price
        self.seed = seed
        self.traders = traders
        self.products = products
        self.book = [OrderBook(product) for product in products]
        self.positions = {trader.name:asset for asset in ("cash", *products) for trader in traders}

    def run_game(self, rounds):
        for round in range(rounds):
            for trader in self.traders:
                # TODO: handle errors
                # TODO: enforce int levels
                # TODO: order limitis (1 order, 2 order, limitless, size prority)
                markets = trader.submit_trades()

    def visualize(self):
        pass # TODO


class BaseTrader():
    def __init__(self, name):  # TODO: add externam id
        self.name = name

    def do_trade(self, round: int, book: Tuple[OrderBook], position: Position) -> List[Order]:  # TODO: add their outstanding positions
        return []

    def __repr__(self):
        pass