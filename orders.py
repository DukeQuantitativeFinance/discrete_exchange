from enum import Enum


class Side(Enum):
    buy = True
    sell = False

class BaseOrder:  # Initialize as a subclass (ie BuyOrder)
    """
    Base order class that is submitted to the Exchange. Contains relevant information.
    Prefered creation is through the BuyOrder, SellOrder subclasses
    """
    def __init__(self, price: int, size: int, product: str, side: Side):
        self.price = price
        self.size = size
        self.product = product
        self.side = side
        self.round = 0
        self.owner = None

    @classmethod
    def from_tuple(cls, tuple, product):
        price, size = tuple
        return cls(price, size, product)

    def __lt__(self, other):  # price time priority
        return (self.price < other.price) == self.side.value or (self.price == other.price and self.round > other.round)

    def __gt__(self, other):
        return (self.price > other.price) == self.side.value or (self.price == other.price and self.round < other.round)

    def __eq__(self, other):
        return self.price == other.price and self.round == other.round

    def __repr__(self):
        if self.side == Side.buy:
            return f"{self.owner} buy {self.size}x${self.price} (round {self.round})"
        else:
            return f"{self.owner} sell {self.size}x${self.price} (round {self.round})"

    def get_deletion(self, amount=-1):
        """
        Generates an order to delete all markets at this level or above
        :param amount the number of markets greater than this size to remove
        :return: A new deletion order
        """
        return DeletionOrder(self.price, amount, self.product, self.side)  # delete all orders up to price


class BuyOrder(BaseOrder):
    def __init__(self, price: int, size: int, product: str):
        super().__init__(price, size, product, Side.buy)


class SellOrder(BaseOrder):
    def __init__(self, price: int, size: int, product: str):
        super().__init__(price, size, product, Side.sell)


class DeletionOrder(BaseOrder):
    def __repr__(self):
        return f"Delete {self.size if self.size >=0 else 'all'} " \
               f"       {'Buy' if self.side else 'Sell'}Orders " \
               f"       at ${self.price} or {'above' if self.side else 'below'}"