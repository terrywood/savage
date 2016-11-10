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


def main():
    user = easytrader.use('gf')
    user.prepare('gf.json')
    print(user.get_position())
    # print(user.sell('512880', price=0, amount=100, entrust_prop=1))


if __name__ == '__main__':
    main()
