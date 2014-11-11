# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction

__all__ = ['Template', 'Product']
__metaclass__ = PoolMeta


class Template:
    __name__ = 'product.template'
    esale_new = fields.Boolean('New', help='Icon New product')
    esale_hot = fields.Boolean('Hot', help='Icon Hot product')
    esale_menus_by_website = fields.Function(fields.Many2Many(
        'esale.catalog.menu', None, None, 'Menus by Website'),
        'get_esale_menus_by_website')

    def get_esale_menus_by_website(self, name):
        '''Get all menus by website (context)'''
        menus = [] # ids
        if not self.esale_menus:
            return menus

        website = None
        if Transaction().context.get('website'):
            website = Transaction().context.get('website')
        if not website:
            return menus

        for menu in self.esale_menus:
            if menu.website.id == website:
                menus.append(menu.id)
        return menus


class Product:
    __name__ = 'product.product'
    add_cart = fields.Boolean('Add Cart', states={
            'readonly': ~Eval('active', True),
            }, depends=['active'],
            help='Available to add cart')

    @staticmethod
    def default_add_cart():
        return True
