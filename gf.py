# -*- coding: utf-8 -*-

import anyjson as json
import click
import dill
import json
import easytrader
import time
import urllib
import urllib.request
from easytrader.log import log
from datetime import datetime, date


def isTradeDay():
    tt = datetime.now().minute % 2
    if tt == 0:
        return True
    day_of_week = datetime.now().weekday()
    if day_of_week < 5:
        h = datetime.now().hour
        if h >= 9 or h < 15:
            return False
        else:
            return False
    else:
        return False


def main():
    work()


def work():
    # url = 'https://xueqiu.com/P/ZH902949'
    # terry test
    while True:
        if isTradeDay():
            log.info('is trade day ready go')
            break
        else:
            log.info('is not trade day sleep 10 minute')
            time.sleep(10)

    url = 'https://xueqiu.com/P/ZH914042'
    headers = ('User-Agent',
               'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/46.0.2490.76 Mobile Safari/537.36')
    balance = 100000
    user = easytrader.use('gf')
    user.prepare('gf.json')
    while True:
        opener = urllib.request.build_opener()
        opener.addheaders = [headers]
        response = opener.open(url)
        try:
            for line in response:
                data = line.decode('utf-8')
                if data.startswith('SNB.cubeInfo'):
                    cube = data.lstrip('SNB.cubeInfo = ')
                    encodedjson = json.loads(cube)
                    rebalancing = encodedjson['sell_rebalancing']
                    id = rebalancing['id']
                    with open('D:\gf\db.txt', 'r') as f:
                        oldId = (f.read()).format()
                        newId = str(id)
                        if oldId != newId:
                            histories = rebalancing['rebalancing_histories']
                            for entity in histories:
                                target_weight = entity['target_weight']
                                weight = entity['weight']
                                if target_weight != weight:
                                    log.info('may be can not deal')
                                    continue
                                price = entity['price']
                                stock_symbol = entity['stock_symbol']
                                stock_symbol = stock_symbol[2:]
                                prev_weight = entity['prev_weight']
                                if prev_weight is None:
                                    prev_weight = 0
                                if weight > prev_weight:
                                    log.info('s 3')
                                    amount = ((((balance * (weight - prev_weight)) / 100) / price) // 100) * 100
                                    # user.buy(stock_symbol, price=price, amount=amount)
                                    message = 'buy ' + str(amount) + ' code ' + stock_symbol
                                    log.info(message)
                                elif weight == 0:
                                    # positions = user.position['data']
                                    heartbeat = user.get_heartbeat_response()
                                    positions = heartbeat['data']
                                    for position in positions:
                                        stock_code = position['stock_code']
                                        log.info('s 4' + stock_code + '<->' + stock_symbol)
                                        if stock_code == stock_symbol:
                                            amount = position['enable_amount']
                                            # user.sell(stock_symbol, price=price, amount=enable_amount)
                                            message = 'sell clear ' + str(amount) + ' code ' + stock_symbol
                                            log.info(message)
                                else:
                                    log.info('s 5')
                                    amount = ((((balance * (prev_weight - weight)) / 100) / price) // 100) * 100
                                    # user.sell(stock_symbol, price=price, amount=amount)
                                    message = 'sell ' + str(amount) + ' code ' + stock_symbol
                                    log.info(message)
                            with open('D:\gf\db.txt', 'w') as f1:
                                f1.write(newId)
                        else:
                            # print('anything no change')
                            pass
                    break
        finally:
            response.close()
        # time.sleep(5)
        if not isTradeDay():
            log.info('today work end ')
            work()

if __name__ == '__main__':
    main()
