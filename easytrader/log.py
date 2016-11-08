# coding:utf8
import logging

log = logging.getLogger('easytrader')
log.setLevel(logging.DEBUG)
log.propagate = False

fmt = logging.Formatter('%(asctime)s [%(levelname)s] %(filename)s %(lineno)s: %(message)s')
ch = logging.StreamHandler()
fh = logging.FileHandler('savage.log')
fh.setFormatter(fmt)
ch.setFormatter(fmt)
ch.setLevel(logging.INFO)
log.handlers.append(ch)
log.handlers.append(fh)
