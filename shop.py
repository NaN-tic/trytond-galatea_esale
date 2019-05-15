# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta
from trytond.i18n import gettext
from trytond.exceptions import UserError

__all__ = ['SaleShop']


class SaleShop(metaclass=PoolMeta):
    __name__ = 'sale.shop'

    @classmethod
    def get_shop_app(cls):
        res = super(SaleShop, cls).get_shop_app()
        res.append(('galatea', 'Galatea'))
        return res

    @staticmethod
    def default_esale_shop_app():
        return 'galatea'

    def import_orders_galatea(self, shop):
        raise UserError(gettext('galatea_esale.msg_not_import_export_method'))

    def export_state_galatea(self, shop):
        """Export State Sale whitout app don't available
        :param shop: Obj
        """
        raise UserError(gettext('galatea_esale.msg_not_import_export_method'))
