# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Not, Bool, And

__all__ = ['Sale', 'SaleLine']
__metaclass__ = PoolMeta


class Sale:
    __name__ = 'sale.sale'
    galatea_user = fields.Many2One('galatea.user', 'Galatea User',
         readonly=True)

    @classmethod
    def get_esale_carriers(cls, shop, party=None, untaxed=0, tax=0, total=0, payment=None):
        '''Available eSale Carriers'''
        return [c.carrier for c in shop.esale_carriers]

    def set_esale_sale(self, data):
        '''Overwrite this method to add more fields in sale object from request.form.data'''
        return self


class SaleLine:
    __name__ = 'sale.line'
    sid = fields.Char('Session')
    galatea_user = fields.Many2One('galatea.user', 'Galatea User', readonly=True)
    product_id = fields.Function(fields.Integer('Product ID'), 'get_product_id')
    template_id = fields.Function(fields.Integer('Template ID'), 'get_template_id')
    shop = fields.Many2One('sale.shop', 'Shop', domain=[
        ('id', 'in', Eval('context', {}).get('shops', [])),
        ])

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()
        cls.party.states['required'] = And((Not(Bool(Eval('sid')))), cls.party.states['required'])
        cls.party.depends.append('sid')

    def get_product_id(self, name):
        '''Return product ID'''
        if self.product:
            return self.product.id
        return None

    def get_template_id(self, name):
        '''Return template ID'''
        if self.product:
            return self.product.template.id
        return None
