from settings import API_KEY, API_SECRET
from binance.client import Client
from binance.enums import *
from decimal import *


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


def buy(currency):
    btc_balance = client.get_account()['balances'][0]['free']
    print(Colors.FAIL + 'Using your full BTC balance: ' +
          btc_balance + Colors.ENDC + '\n')
    btc_amount = float(btc_balance)

    symbol = currency + 'BTC'
    info = client.get_symbol_info(currency+'BTC')

    minimum = float(info['filters'][2]['minQty'])
    price_jump = float(info['filters'][0]['tickSize'])
    symbol = currency + 'BTC'
    buy_price = float(client.get_orderbook_ticker(symbol=symbol)['askPrice'])
    if minimum < 1:
        quantity = Decimal(
            btc_amount/buy_price).quantize(Decimal(str(minimum)), rounding=ROUND_DOWN)
    else:
        quantity = Decimal(
            btc_amount/buy_price).quantize(Decimal('1.'), rounding=ROUND_DOWN)

    # Change to client.create_order
    client.create_test_order(
        symbol=symbol,
        side=SIDE_BUY,
        type=ORDER_TYPE_MARKET,
        quantity=quantity
    )

    print(
        Colors.HEADER +
        '# ------------------------------------------------------------------------- #'
        + Colors.ENDC
    )
    print(
        Colors.HEADER + '#  ' +
        Colors.OKGREEN + 'BUY order of ' + str(quantity) + ' ' +
        str(symbol) + ' set @ ' +
        str(buy_price) + ' BTC ' + ' totalling ' +
        str(buy_price*float(quantity)) + ' BTC'
    )

    sell_price = Decimal(
        1.5*buy_price).quantize(Decimal(str(price_jump)), rounding=ROUND_DOWN)

    # Change to client.create_order
    client.create_test_order(
        symbol=currency + 'BTC',
        side=SIDE_SELL,
        type=ORDER_TYPE_LIMIT,
        timeInForce=TIME_IN_FORCE_GTC,
        quantity=quantity,
        price=sell_price
    )

    print(
        Colors.HEADER + '#  ' +
        Colors.OKCYAN + 'SELL order of ' + str(quantity) + ' ' +
        str(symbol) + ' set @ ' +
        str(sell_price) + ' BTC ' + ' totalling ' +
        str(sell_price*quantity) + ' BTC'
    )
    print(
        Colors.HEADER +
        '# ------------------------------------------------------------------------- #'
        + Colors.ENDC
    )


print(Colors.BOLD + Colors.OKBLUE + 'Enter a coin abbreviation: ' + Colors.ENDC)
buy(input().upper())
