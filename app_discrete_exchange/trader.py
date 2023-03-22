from typing import *

from .book import PublicBook
from .orders import BaseOrder, BuyOrder, SellOrder


class BaseTrader:
    def __init__(self, name):
        self.name = name

    def trade(self, round: int, book: dict[str, PublicBook], outstanding_markets: Dict[str, PublicBook], position: dict[str, int]) -> list[BaseOrder]:
        """
        Prompt the trader for their actions given the current state of the exchange
        Formatting: dict[str, PublicBook] = {"product", (bids=((price, size)...), offers=((price, size)...))
        :param round: The current round number
        :param book: dictionary representing the open positions on each market.
        :param outstanding_markets: dictionary representing your outstanding markets
        :param position: dictionary representing your outstanding positions on each asset (cash & products)
        :return: a list of orders. These can be buy, sell, or deletions
        """
        return []

    def __repr__(self):
        return self.name


class DumbTrader(BaseTrader):
    def trade(self, round: int, book: dict[str, PublicBook], outstanding_markets: Dict[str, PublicBook], position: dict[str, int]) -> list[BaseOrder]:
        return [BuyOrder(round, 10, "test"), SellOrder(100-round, 10, "test")]

class BoringTrader(BaseTrader):
    def trade(self, round: int, book: dict[str, PublicBook], outstanding_markets: Dict[str, PublicBook], position: dict[str, int]) -> list[BaseOrder]:
        return [BuyOrder(40, 10, "test"), SellOrder(60, 10, "test")]
