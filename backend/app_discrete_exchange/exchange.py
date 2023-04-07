import random
from copy import deepcopy
from .book import OrderBook
from .orders import *
from .trader import BaseTrader


class Exchange:
    MAX_ORDER_SIZE = 1000
    MIN_PRICE = 0
    MAX_PRICE = 100
    def __init__(self, products, *traders: BaseTrader):
        self.traders = traders
        self.products = products
        self.positions = {trader: {asset: 0 for asset in ["cash", *products]} for trader in traders}
        self.books = {product: OrderBook(product, self.positions) for product in products}
        self.outstanding_orders = {trader.name: [] for trader in traders}

    def run_game(self, rounds):
        """
        Run the game for the specified rounds. A round consists of reading orders, validating, deleting, and processing
        """
        for round in range(rounds):
            round_orders: list[BaseOrder] = []
            round_deletions: list[DeletionOrder] = []
            books = [self.books[book].public() for book in self.books]
            for trader in self.traders:
                try:
                    public = {product:book for product, book in zip(self.products, books)}
                    outstanding = {product:self.books[product].get_outstanding(trader) for product in self.products}
                    orders = trader.trade(round, public, outstanding, deepcopy(self.positions[trader]))
                    orders, deletions = self.validate_orders(orders, trader, round)
                    round_orders.extend(orders)
                    round_deletions.extend(deletions)
                except Exception as e:
                    print(f"Trader {trader.name} encountered {e}")
            for deletion in round_deletions:
                self.books[deletion.product].deletion_order(deletion)
            random.shuffle(round_orders)
            for order in round_orders:
                self.books[order.product].new_order(order)

    def validate_orders(self, orders: list[BaseOrder], trader: BaseTrader, round: int) -> tuple[list[BaseOrder], list[DeletionOrder]]:
        """
        Confirm that trader isn't doiing anything crazy and separate deletions
        - set round and owner
        - copy to prevent future manipulation
        - force size and price to be ints
        - prevent excessive sizing
        :param orders: The raw trades sent by trader
        :param trader: the trader object who
        :param round: round these orders were created
        :return: the buy/sell order, the deletion orders
        """
        out_orders = []
        out_deletions = []

        for order in orders:
            order = deepcopy(order)
            order.owner = trader
            order.round = round
            order.price = int(order.price)
            order.size = min(int(order.size), self.MAX_ORDER_SIZE)
            if isinstance(order, DeletionOrder):
                out_deletions.append(order)  # have to copy to prevent later order manipulation
            elif self.MIN_PRICE < order.price < self.MAX_PRICE:
                out_orders.append(order)
        return out_orders, out_deletions

    # TODO: implement visuals and history

    def get_pnl(self, trader):
        return self.positions[trader]['cash']        