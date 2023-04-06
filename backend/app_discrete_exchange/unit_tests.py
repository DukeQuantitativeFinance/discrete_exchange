from book import *
from exchange import *
from orders import *
from trader import *


def test_order():
    # Buy order test
    buy1 = BuyOrder(50, 100, "test")
    buy2 = BuyOrder(20, 10, "test")
    buy3 = BuyOrder(50, 100, "test")
    assert buy1 > buy2
    assert buy2 < buy1
    assert buy1 == buy3
    buy1.round = 1
    buy3.round = 3
    assert buy1 > buy3
    assert buy3 < buy1
    assert not buy1 == buy3
    assert not isinstance(buy1, DeletionOrder)

    # Sell order test
    sell1 = SellOrder(50, 100, "test")
    sell2 = SellOrder(20, 10, "test")
    sell3 = SellOrder(50, 100, "test")
    assert sell1 < sell2
    assert sell2 > sell1
    assert sell1 == sell3
    sell1.round = 1
    sell3.round = 3
    assert sell1 > sell3
    assert sell3 < sell1
    assert not sell1 == sell3
    assert not isinstance(sell1, DeletionOrder)

    # Deletion test
    del1 = DeletionOrder(50,100,"test",Side.buy)
    assert isinstance(del1, DeletionOrder)


def test_exchange():
    t1 = DumbTrader('t1')
    t2 = BoringTrader('t2')
    exchange = Exchange(["test"], t1, t2)
    exchange.run_game(100)


def test_book():
    t1 = BaseTrader("t1")
    t2 = BaseTrader("t2")
    t3 = BaseTrader("t3")

    buy1 = BuyOrder(90, 100, "test")
    buy1.round = 1
    buy1.owner = t1
    buy2 = BuyOrder(95, 5, "test")
    buy2.round = 1
    buy2.owner = t3
    buy3 = BuyOrder(90, 10, "test")
    buy3.round = 2
    buy3.owner = t1
    buy4 = BuyOrder(50, 5, "test")
    sell1 = SellOrder(10, 10, "test")
    sell1.round = 1
    sell1.owner = t2

    assests = {t1: {"cash": 0, "test": 0}, t2: {"cash": 0, "test": 0}, t3: {"cash": 0, "test": 0}}
    a2 = deepcopy(assests)
    a3 = deepcopy(assests)

    book = OrderBook("test", assests)
    book.new_order(buy1)
    book.new_order(buy2)
    book.new_order(buy4)
    book.new_order(buy3)
    book.new_order(sell1)
    assert assests == {t1: {'cash': -450, 'test': 5}, t2: {'cash': 925, 'test': -10}, t3: {'cash': -475, 'test': 5}}

    book2 = OrderBook("test", a2)
    buy1 = BuyOrder(90, 100, "test")
    buy2 = BuyOrder(95, 5, "test")
    del1 = buy1.get_deletion()
    book2.new_order(buy1)
    book2.new_order(buy2)
    book2.deletion_order(del1)
    assert str(book2) == "test book: 0 bids & 0 offers"
    buy1 = BuyOrder(90, 100, "test")
    buy2 = BuyOrder(95, 5, "test")
    del1 = buy2.get_deletion()
    book2.new_order(buy1)
    book2.new_order(buy2)
    book2.deletion_order(del1)
    del2 = DeletionOrder(100, -1, "test", Side.buy)
    book2.deletion_order(del2)
    assert str(book2.public()) == "PublicBook(bids=((90, 100),), offers=())"
    del1 = DeletionOrder(80, 50, "test", Side.buy)
    book2.deletion_order(del1)
    assert str(book2.public()) == "PublicBook(bids=((90, 50),), offers=())"
    sell1 = SellOrder(95, 10, "test")
    del2 = DeletionOrder(99, 100, "test", Side.sell)
    book2.new_order(sell1)
    book2.deletion_order(del2)
    assert str(book2.public()) == "PublicBook(bids=(), offers=((95, 10),))"

    # test time priority deletion
    book3 = OrderBook("test", a3)
    buy1 = BuyOrder(50, 5, "test")
    buy1.round = 1
    buy2 = BuyOrder(50, 5, "test")
    buy2.round = 2
    del1 = DeletionOrder(50, 4, "test", Side.buy)
    book3.new_order(buy1)
    book3.new_order(buy2)
    book3.deletion_order(del1)
    print(book3.bids)
    assert str(book3.bids) == "[None buy 5x$50 (round 1), None buy 1x$50 (round 2)]"


def test_all():
    test_order()
    test_book()
    test_exchange()