# built-in
from decimal import Decimal, ROUND_DOWN

# third-party
from binance.client import Client
from binance.exceptions import BinanceOrderException
from binance.enums import SIDE_BUY, SIDE_SELL, ORDER_TYPE_MARKET, ORDER_TYPE_LIMIT, TIME_IN_FORCE_GTC

# local
from settings import API_KEY, API_SECRET

client = Client(API_KEY, API_SECRET)

class Colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def color_print(color, text):
    print(color + text + Colors.ENDC)


def get_btc_balance():
    return float(client.get_account()['balances'][0]['free'])


def get_symbol_info(symbol):
    return client.get_symbol_info(symbol)


def calculate_quantity(btc_amount, buy_price, minimum):
    if minimum < 1:
        return Decimal(btc_amount / buy_price).quantize(Decimal(str(minimum)), rounding=ROUND_DOWN)
    else:
        return Decimal(btc_amount / buy_price).quantize(Decimal('1.'), rounding=ROUND_DOWN)


def create_order(symbol, side, order_type, quantity, price=None):
    order = {
        "symbol": symbol,
        "side": side,
        "type": order_type,
        "quantity": quantity
    }
    if price:
        order["price"] = price
        order["timeInForce"] = TIME_IN_FORCE_GTC

    client.create_test_order(**order)


def create_buy_order(symbol, quantity):
    try:
        create_order(symbol, SIDE_BUY, ORDER_TYPE_MARKET, quantity)
        color_print(Colors.HEADER, '# ------------------------------------------------------------------------- #')
        color_print(Colors.OKGREEN, f'BUY order of {quantity} {symbol} set @ {quantity} BTC totalling {quantity} BTC')
    except BinanceOrderException as e:
        color_print(Colors.FAIL, str(e.status_code))
        color_print(Colors.FAIL, e.message)


def create_sell_order(symbol, quantity, sell_price):
    try:
        create_order(symbol, SIDE_SELL, ORDER_TYPE_LIMIT, quantity, sell_price)
        color_print(Colors.HEADER, '# ------------------------------------------------------------------------- #')
        color_print(Colors.OKCYAN, f'SELL order of {quantity} {symbol} set @ {sell_price} BTC totalling {sell_price*quantity} BTC')
    except BinanceOrderException as e:
        color_print(Colors.FAIL, str(e.status_code))
        color_print(Colors.FAIL, e.message)


def main():
    color_print(Colors.BOLD + Colors.OKBLUE, 'Enter a coin abbreviation: ')
    currency = input().upper()
    btc_balance = get_btc_balance()
    color_print(Colors.FAIL, f'Using your full BTC balance: {btc_balance}')

    symbol = currency + 'BTC'
    info = get_symbol_info(symbol)

    minimum = float(info['filters'][2]['minQty'])
    price_jump = float(info['filters'][0]['tickSize'])
    buy_price = float(client.get_orderbook_ticker(symbol=symbol)['askPrice'])
    quantity = calculate_quantity(btc_balance, buy_price, minimum)

    create_buy_order(symbol, quantity)

    sell_price = Decimal(1.5 * buy_price).quantize(Decimal(str(price_jump)), rounding=ROUND_DOWN)
    create_sell_order(symbol, quantity, sell_price)


if __name__ == "__main__":
    main()