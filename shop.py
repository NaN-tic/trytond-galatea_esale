#This file is part galatea_esale module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

from decimal import Decimal
import time

__all__ = ['SaleShop']
__metaclass__ = PoolMeta


class SaleShop:
    __name__ = 'sale.shop'

    @classmethod
    def get_shop_app(cls):
        res = super(SaleShop, cls).get_shop_app()
        res.append(('galatea','Galatea'))
        return res

    @staticmethod
    def default_esale_shop_app():
        return 'galatea'
