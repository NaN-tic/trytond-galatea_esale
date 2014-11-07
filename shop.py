# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import PoolMeta

__all__ = ['SaleShop']
__metaclass__ = PoolMeta


class SaleShop:
    __name__ = 'sale.shop'

    @classmethod
    def __setup__(cls):
        super(SaleShop, cls).__setup__()
        cls._error_messages.update({
            'not_import': 'Functions import/export in Galatea Shops are ' \
            'not necessary',
        })

    @classmethod
    def get_shop_app(cls):
        res = super(SaleShop, cls).get_shop_app()
        res.append(('galatea','Galatea'))
        return res

    @staticmethod
    def default_esale_shop_app():
        return 'galatea'

    def import_orders_galatea(self, shop):
        self.raise_user_error('not_import')

    def export_state_galatea(self, shop):
        """Export State Sale whitout app don't available
        :param shop: Obj
        """
        self.raise_user_error('not_import')
