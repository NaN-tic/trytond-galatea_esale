# This file is part of the galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields

__all__ = ['SaleCart']
__metaclass__ = PoolMeta


class SaleCart:
    __name__ = 'sale.cart'
    sid = fields.Char('Session', readonly=True)
    galatea_user = fields.Many2One('galatea.user', 'Galatea User', readonly=True)
    product_id = fields.Function(fields.Integer('Product ID'), 'get_product_id')

    def get_product_id(self, name):
        '''Return product ID'''
        if self.product:
            return self.product.id
        return None
