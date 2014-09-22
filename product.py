#This file is part galatea_esale module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval

__all__ = ['Template', 'Product']
__metaclass__ = PoolMeta


class Template:
    __name__ = 'product.template'
    esale_new = fields.Boolean('New', help='Icon New product')
    esale_hot = fields.Boolean('Hot', help='Icon Hot product')


class Product:
    __name__ = 'product.product'
    add_cart = fields.Boolean('Add Cart', states={
            'readonly': ~Eval('active', True),
            }, depends=['active'],
            help='Available to add cart')

    @staticmethod
    def default_add_cart():
        return True
