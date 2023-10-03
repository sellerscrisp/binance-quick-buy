import logging
from decimal import Decimal, ROUND_DOWN
from typing import Dict, Union

from binance.client import Client
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC
from binance.exceptions import BinanceOrderException

from settings import API_KEY, API_SECRET

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class BinanceTrader:
    
    def __init__(self):
        self.client = Client(API_KEY, API_SECRET)
        self.btc_balance = self.get_btc_balance()
        self.currency = ""
        self.symbol = ""
        self.minimum = 0.0
        self.price_jump = 0.0
        self.buy_price = 0.0
        self.quantity = 0.0

    def get_btc_balance(self) -> float:
        return float(self.client.get_account()['balances'][0]['free'])

    def get_symbol_info(self) -> Dict[str, Union[str, float]]:
        return self.client.get_symbol_info(self.symbol)

    def calculate_quantity(self) -> Decimal:
        if self.minimum < 1:
            return Decimal(self.btc_balance / self.buy_price).quantize(Decimal(str(self.minimum)), rounding=ROUND_DOWN)
        return Decimal(self.btc_balance / self.buy_price).quantize(Decimal('1.'), rounding=ROUND_DOWN)

    def create_order(self, side: str, order_type: str, price: float = None):
        order = {
            "symbol": self.symbol,
            "side": side,
            "type": order_type,
            "quantity": self.quantity
        }
        if price:
            order["price"] = price
            order["timeInForce"] = TIME_IN_FORCE_GTC
        self.client.create_test_order(**order)

    def initialize_trade(self):
        self.currency = input("Enter a coin abbreviation: ").upper()
        logger.info(f"Using your full BTC balance: {self.btc_balance}")
        self.symbol = f"{self.currency}BTC"
        info = self.get_symbol_info()
        self.minimum = float(info['filters'][2]['minQty'])
        self.price_jump = float(info['filters'][0]['tickSize'])
        self.buy_price = float(self.client.get_orderbook_ticker(symbol=self.symbol)['askPrice'])
        self.quantity = self.calculate_quantity()

    def execute_trade(self):
        try:
            self.create_order(SIDE_BUY, ORDER_TYPE_MARKET)
            logger.info(f'BUY order of {self.quantity} {self.symbol} set')
        except BinanceOrderException as e:
            logger.error(f"{e.status_code} - {e.message}")

        sell_price = Decimal(1.5 * self.buy_price).quantize(Decimal(str(self.price_jump)), rounding=ROUND_DOWN)
        try:
            self.create_order(SIDE_SELL, ORDER_TYPE_LIMIT, sell_price)
            logger.info(f'SELL order of {self.quantity} {self.symbol} set')
        except BinanceOrderException as e:
            logger.error(f"{e.status_code} - {e.message}")


def main():
    trader = BinanceTrader()
    trader.initialize_trade()
    trader.execute_trade()


if __name__ == "__main__":
    main()
