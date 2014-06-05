#This file is part galatea_esale module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta

__all__ = ['Template']
__metaclass__ = PoolMeta


class Template:
    __name__ = 'product.template'
    esale_hot = fields.Boolean('Hot', help='Icon Hot product')
