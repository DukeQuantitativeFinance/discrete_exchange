from .orders import *
from typing import NamedTuple


class PublicBook(NamedTuple):
    """
    Datastructure to immutably represent outstanding orders
    """
    bids: tuple[tuple[int, int]]  # ((price, size), ...)
    offers: tuple[tuple[int, int]]  # ((price, size), ...)

class OrderBook:
    """
    Internal class to manage the markets for a product
    """
    def __init__(self, product, positions):
        """
        Initialize an order book
        :param product: name of the product this book represents
        :param positions: positions of each trader. {trader: {asset: amount}}
        """
        self.positions = positions
        self.product = product
        self.bids: list[BuyOrder] = []  # buy prices - high to low
        self.offers: list[SellOrder] = []  # sell prices - low to high

    def new_order(self, order: BaseOrder) -> None:
        """ Process a new order by searching for matching offers and then inserting into list for future matches """
        self.match_order(order)
        self.insert_order(order)

    def insert_order(self, order: BaseOrder) -> None:
        """ Insert order into its time prority spot on the list"""
        assert not isinstance(order, DeletionOrder)
        if order.size <= 0: return
        if order.side == Side.buy:
            for i, bid in enumerate(self.bids):
                if order > bid:
                    self.bids.insert(i, order)
                    break
            else:
                self.bids.append(order)
        else:
            for i, offer in enumerate(self.offers):
                if order > offer:
                    self.offers.insert(i, order)
                    break
            else:
                self.offers.append(order)

    def match_order(self, order: BaseOrder) -> None:
        """ Try to match order with corresponding offers ie buy & sell """
        if order.side == Side.buy:
            to_remove = []
            for offer in self.offers:
                if offer.price > order.price: break  # no more matching offers
                sizing = min(order.size, offer.size)
                offer.size -= sizing; order.size -= sizing
                # adjust assets
                # print(f"Round {order.round}: {order.owner} offers {sizing} for ${offer.price} to {offer.owner}")
                self.positions[offer.owner]["cash"] += offer.price * sizing; self.positions[offer.owner][offer.product] -= sizing
                self.positions[order.owner]["cash"] -= offer.price * sizing; self.positions[order.owner][offer.product] += sizing
                # edit markets
                if offer.size <= 0: to_remove.append(offer)
                if order.size <= 0: break
            for offer in to_remove:
                self.offers.remove(offer)
        else:
            to_remove = []
            for bid in self.bids:
                if bid.price < order.price: break  # no more matching offers
                sizing = min(order.size, bid.size)
                bid.size -= sizing
                order.size -= sizing
                # adjust assets
                # print(f"Round {order.round}: {order.owner} bids {sizing} for ${bid.price} to {bid.owner}")
                self.positions[bid.owner]["cash"] -= bid.price * sizing
                self.positions[bid.owner][bid.product] += sizing
                self.positions[order.owner]["cash"] += bid.price * sizing
                self.positions[order.owner][bid.product] -= sizing
                # edit markets
                if bid.size <= 0: to_remove.append(bid)
                if order.size <= 0: break
            for offer in to_remove:
                self.bids.remove(offer)

    def deletion_order(self, order: DeletionOrder) -> None:
        """ A request to delete a max of [order.size] orders which exceed [order.price]. Exceed is lower sells and higher bids """
        assert isinstance(order, DeletionOrder)
        if order.size == -1: order.size = 1e9
        deleting_orders = list(filter(lambda o: o.owner is order.owner and (o.price >= order.price if order.side == Side.buy else o.price <= order.price), self.bids))
        # setup priority structure
        levels = []
        level = []
        price = -1
        for bid in deleting_orders:
            if bid.price != price and price != -1:
                levels.append(level)
                level = [bid]
            else:
                level.append(bid)
            price = bid.price
        levels.append(level)

        # pop from structure
        for level in levels:
            while level:
                b = level.pop()
                b.size, order.size = b.size - order.size, order.size - b.size
                if b.size <= 0: self.bids.remove(b)
                if order.size <= 0: break
            if order.size <= 0:
                break

    def get_outstanding(self, trader) -> PublicBook:
        """ Get all the orders in this book from a given trader. *This should be copied before being passed back* """
        bids = [(bid.price, bid.size) for bid in filter(lambda o: o.owner is trader, self.bids)]
        offers = [(offer.price, offer.size) for offer in filter(lambda o: o.owner is trader, self.offers)]
        return PublicBook(bids=tuple(bids), offers=tuple(offers))

    def public(self) -> PublicBook:
        """
        Create a copy of the order book to send to each trader
        :return: bids: [(price, size),...], offers: [(price, size),...]
        """
        bids = []
        offers = []
        price = -1
        size = 0
        for bid in self.bids:
            if bid.price == price:
                size += bid.size
            else:
                if price != -1:
                    bids.append((price, size))
                size = bid.size
                price = bid.price
        if price != -1: bids.append((price, size))
        price = -1
        for offer in self.offers:
            if offer.price == price:
                size += offer.size
            else:
                if price != -1:
                    offers.append((price, size))
                size = offer.size
                price = offer.price
        if price != -1: offers.append((price, size))
        return PublicBook(bids=tuple(bids), offers=tuple(offers))

    def __repr__(self):
        return f"{self.product} book: {len(self.bids)} bids & {len(self.offers)} offers"
