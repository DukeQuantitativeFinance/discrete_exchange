from dataclasses import dataclass
from typing import *
from enum import Enum


class Side(Enum):
    buy = True
    sell = False

@dataclass
class BaseOrder:  # Initialize as a subclass (ie BuyOrder)
    """
    Base order class that is submitted to the Exchange. Contains relevant information.
    Perfered creation is through the BuyOrder, SellOrder subclasses
    """
    price: int
    size: int
    product: str
    side: Side
    round = 0  # set by exchange
    owner = None  # set by exchange (type of BaseTrader

    def __lt__(self, other: Self):  # price time priority
        return self.price < other.price == self.side or (self.price == other.price and self.round > other.round)

    def __gt__(self, other: Self):
        return self.price > other.price  == self.side or (self.price == other.price and self.round < other.round)

    def __eq__(self, other):
        return self.price == other.price and self.round == other.round

    def __repr__(self):
        if self.side == Side.buy:
            return f"{self.owner} buy {self.size}x${self.price} (round {self.round})"
        else:
            return f"{self.owner} sell {self.size}x${self.price} (round {self.round})"

    def get_deletion(self):
        """
        Generates an order to delete all markets at this level or above
        :return: A new deletion order
        """
        return DeletionOrder(self.price, -1, self.product, self.side)  # delete all orders up to price


class BuyOrder(BaseOrder):
    side = Side.buy


class SellOrder(BaseOrder):
    side = Side.sell


class DeletionOrder(BaseOrder):
    def __repr__(self):
        return f"Delete {self.size if self.size >=0 else 'all'} " \
               f"       {'Buy' if self.side else 'Sell'}Orders " \
               f"       at ${self.price} or {'above' if self.side else 'below'}"