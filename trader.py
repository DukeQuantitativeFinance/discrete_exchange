import typing

class BaseTrader():
    def __init__(self, name):
        pass

    def update_history(self, orders):
        """
        Provide the details of the trades in the previous rounds

        :return:
        """
        pass

    def submit_trades(self) -> typing.List<Market>:
        pass

    def set_api(self, api: ExchangeAPI):
        pass

    def __repr__(self):
        pass