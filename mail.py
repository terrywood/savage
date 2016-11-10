# -*- coding: utf-8 -*-
import datetime
import email
import email.header
import imaplib
import json

import easytrader.util
from easytrader.log import log

host = "imap.163.com"
username = "qq3532619@163.com"
password = "abcabc123123"


def parse(content):
    index1 = content.find("Hold1") - 2
    index2 = content.find("Total_profit_rate") - 2
    working = json.loads(content[0:index1])
    position = json.loads(content[index1:index2])
    log.info(working)
    log.info(position)
    buy_list = []
    for code in working['buy']:
        for tick in position:
            if position[tick]['code'] == code:
                entity = position[tick]
                buy_list.append(entity)
                break

    working['buy'] = buy_list
    return working


def mail():
    content = None
    conn = imaplib.IMAP4(host)
    conn.login(username, password)
    conn.select()

    # date = (datetime.date.today() - datetime.timedelta(1)).strftime("%d-%b-%Y")
    # result, data = mail.uid('search', None, '(SENTSINCE {date})'.format(date=date))
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
        # log.info(message_id)
        fr = email.utils.parseaddr(msg['From'])[1]
        if fr != 'ants2016@vip.163.com':
            continue
        hdr = email.header.make_header(email.header.decode_header(msg['Subject']))
        subject = str(hdr)
        if not subject.startswith("Ant_001"):
            continue
        log.info('Message %s: %s' % (num, subject))
        date_tuple = email.utils.parsedate_tz(msg['Date'])
        if date_tuple:
            local_date = datetime.datetime.fromtimestamp(email.utils.mktime_tz(date_tuple))
            if not easytrader.util.is_today(local_date):
                continue
        else:
            log.warn('can not get date tuple')
            continue
        message_id = msg.get('Message-ID')
        with open('D:\gf\mail.txt', 'w') as f1:
            old_id = (f1.read()).format()
            if old_id == message_id :
                log.info('mail is handled')
                continue
            else:
                f1.write(message_id)

        for part in msg.walk():
            content = part.get_payload(decode=True).decode()
            content = content[0:content.find("\n")]
    conn.close()
    conn.logout()
    return parse(content)

if __name__ == '__main__':
    parse(
        '{"date": "2016-11-09", "sell": ["002627.XSHE"], "buy": ["002205.XSHE"]}{"Hold1": {"code": "002205.XSHE", "total_amount": 1300, "Weight": 23.666299865955008, "Cost": 29.89}, "Hold2": {"code": "600213.XSHG", "total_amount": 2600, "Weight": 24.562210045135213, "Cost": 14.81}, "Hold3": {"code": "600781.XSHG", "total_amount": 2100, "Weight": 24.206041532785829, "Cost": 18.24}, "Hold4": {"code": "000713.XSHE", "total_amount": 3300, "Weight": 23.909641024221109, "Cost": 11.22}}{"Total_profit_rate": "63%"}')
