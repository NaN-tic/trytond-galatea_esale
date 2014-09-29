#This file is part galatea_esale module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['GalateaWebSite', 'GalateaUser']
__metaclass__ = PoolMeta


class GalateaWebSite:
    __name__ = "galatea.website"
    esale_menu = fields.Many2One('esale.catalog.menu', 'Main Menu', required=True,
        help='Main menu product catalog')


class GalateaUser:
    __name__ = "galatea.user"
    invoice_address = fields.Many2One('party.address', 'Invoice Address',
        help='Default Invoice Address')
    shipment_address = fields.Many2One('party.address', 'Shipment Address',
        help='Default Shipment Address')
    show_price = fields.Boolean('Show Price',
        help='Allow show prices (Global guest price configuration is not active')
    b2b = fields.Boolean('B2B',
        help='Allow views or data from B2B customers')

    @staticmethod
    def default_show_price():
        return True
