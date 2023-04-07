from typing import *

from .book import PublicBook
from .orders import BaseOrder, BuyOrder, SellOrder
from .trader import BaseTrader

class Trader(BaseTrader):
    def __init__(self):
        self.center = 100
        self.sizing = 100
        self.prev_positions = None

    def trade(self, round: int, book: dict[str, PublicBook], outstanding_markets: Dict[str, PublicBook], position: dict[str, int]) -> list[BaseOrder]:
        orders = list()

        # initial positions
        if self.prev_positions is None:
            for key in position:
                self.prev_positions[key] = 0
                for i in range(1, 20):
                    orders.append(BuyOrder(self.center - i, self.sizing, key))
                    orders.append(SellOrder(self.center + i, self.sizing, key))
            return orders

        # update books
        for key in position:
            pos = position[key]
            prev = self.prev_positions[key]
            fade_amount = pos // self.sizing - prev // self.sizing  # when a full order sizing has been hit
            center = self.center - position[key] // self.sizing
            if fade_amount > 0:  # Price goes down as my bids have been bought
                for i in range(1, fade_amount+1):
                    orders.append(SellOrder(center + i, self.sizing, key))
            elif fade_amount < 0:  # Price goes up as my asks have been sold
                for i in range(1, -fade_amount + 1):
                    orders.append(SellOrder(center - i, self.sizing, key))
        return orders