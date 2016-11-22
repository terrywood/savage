# -*- coding: utf-8 -*-
import email
import email.header
import imaplib
import json
import time
from datetime import datetime

import easytrader.util
from easytrader.log import log

balance = 50000
host = "imap.163.com"
username = "qq3532619@163.com"
password = "*********"
group = "Ant_001"


def parse(content):
    index1 = content.find("Hold1") - 2
    index2 = content.find("Total_profit_rate") - 2
    if index1 > 0:
        working = json.loads(content[0:index1])
        position = json.loads(content[index1:index2])
        buy_list = []
        for code in working['buy']:
            for tick in position:
                if position[tick]['code'] == code:
                    entity = position[tick]
                    buy_list.append(entity)
                    break

        working['buy'] = buy_list
        return working
    else:
        return json.loads(content[0:index2])


def mail():
    content = None
    conn = imaplib.IMAP4(host)
    conn.login(username, password)
    conn.select()
    typ, data = conn.search(None, 'ALL')
    if typ != 'OK':
        log.warn("No messages found!")
        return

    # typ, data = conn.search(None, '(FROM "ants2016")')
    for num in data[0].split():
        # typ, data = conn.fetch(num, '(RFC822)')
        typ, data = conn.fetch(num, '(RFC822)')
        if typ != 'OK':
            log.warn("ERROR getting message", num)
            return
        msg = email.message_from_bytes(data[0][1])
        message_id = msg.get('Message-ID')
        if 'vip.163.com' not in message_id:
            continue
        log.info(message_id)
        fr = email.utils.parseaddr(msg['From'])[1]
        if fr != 'ants2016@vip.163.com':
            continue
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        if not subject.startswith(group):
            continue
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            if not easytrader.util.is_today(local_date):
                continue
        else:
            log.warn('can not get date tuple')
            continue
        with open('D:\gf\mail.txt', 'r') as f1:
            old_id = (f1.read()).format()
            if old_id == message_id:
                log.info('mail is handled')
                content = '{"date": "", "sell": [], "buy": []}{"Total_profit_rate": "0%"}'
                break
            else:
                with open('D:\gf\mail.txt', 'w') as f2:
                    f2.write(message_id)

        for part in msg.walk():
            content = part.get_payload(decode=True).decode()
            content = content[0:content.find("\n")]
    conn.close()
    conn.logout()

    if content is None:
        return None
    else:
        return parse(content)


def balk():
    while True:
        if easytrader.util.is_trade_date():
            if datetime.now().hour > 9:
                break
            elif datetime.now().minute > 26 and datetime.now().hour == 9:
                log.info('is trade day ready')
                break
            else:
                time.sleep(30)
        else:
            log.info('is not trade day sleep 10 minute')
            time.sleep(600)


def main():
    data = None
    balk()
    log.info("go go go")

    while True:
        data = mail()
        # data = parse('{"date": "2016-11-09", "sell": ["000210.xhae"], "buy": []}{"Total_profit_rate": "63%"}')
        if data is None:
            time.sleep(30)
        else:
            break

    user = easytrader.use('gf')
    user.prepare('gf.json')
    positions = user.get_position()
    log.info(positions)
    log.info(data)
    for sell_code in data['sell']:
        sell_code = sell_code[0:6].format()
        message = 'sell clear  code ' + sell_code
        log.info(message)
        for position in positions['data']:
            stock_code = position['stock_code']
            if stock_code == sell_code:
                amount = position['enable_amount']
                last_price = position['last_price']
                # result = user.sell(sell_code, price=last_price, amount=amount)
                # log.info(result)
                message = 'sell clear code = ' + sell_code + ' amount=' + amount + ' last price=' + last_price
                log.info(message)
                break

    for buy_entity in data['buy']:
        buy_code = buy_entity['code']
        buy_code = buy_code[0:6].format()
        volume = buy_entity['Weight'] * balance / 100
        cost = buy_entity['Cost']
        # result = user.buy(buy_code, price=cost, volume=volume)
        # log.info(result)
        message = 'buy  code=' + buy_code + ' balance=' + str(volume) + ' last price=' + str(cost)
        log.info(message)
    log.info("ant working ending")


if __name__ == '__main__':
    main()
