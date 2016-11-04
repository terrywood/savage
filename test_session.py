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
    while True:
        log.info(user.position)
        time.sleep(1)


if __name__ == '__main__':
    main()
