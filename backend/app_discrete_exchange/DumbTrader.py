from typing import *

from .book import PublicBook
from .orders import BaseOrder, BuyOrder, SellOrder
from .trader import BaseTrader

class Trader(BaseTrader):
    def trade(self, round: int, book: dict[str, PublicBook], outstanding_markets: Dict[str, PublicBook], position: dict[str, int]) -> list[BaseOrder]:
        return [BuyOrder(round, 10, "test"), SellOrder(100-round, 10, "test")]