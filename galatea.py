# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval

__all__ = ['GalateaWebSite', 'GalateaUser']


class GalateaWebSite(metaclass=PoolMeta):
    __name__ = "galatea.website"
    esale_menu = fields.Many2One('esale.catalog.menu', 'Main Menu', required=True,
        help='Main menu of product catalog')
    esale_stock = fields.Boolean('Stock',
        help='Manage Stock')
    esale_stock_qty = fields.Selection([
        ('quantity', 'Quantity'),
        ('forecast_quantity', 'Forecast Quantity'),
        ], 'Quantity Stock', states={
            'invisible': ~Eval('esale_stock', True),
        },
        help='Manage Stock is Product Quantity or Product Forecast Quantity')
    esale_category_menu = fields.Many2One('product.category',
        'Catalog Category Menu', domain=[
            ('esale_active', '=', True),
        ], help='Main menu of catalog category')

    @staticmethod
    def default_esale_stock_qty():
        return 'quantity'


class GalateaUser(metaclass=PoolMeta):
    __name__ = "galatea.user"
    invoice_address = fields.Many2One('party.address', 'Invoice Address',
        domain=[('party', '=', Eval('party')), ('invoice', '=', True)],
        depends=['party'], help='Default Invoice Address')
    shipment_address = fields.Many2One('party.address', 'Shipment Address',
        domain=[('party', '=', Eval('party')), ('delivery', '=', True)],
        depends=['party'], help='Default Shipment Address')
    b2b = fields.Boolean('B2B',
        help='Allow views or data from B2B customers')

    @classmethod
    def signal_login(cls, user, session=None, website=None):
        """Flask signal to login
        Update cart prices when user login
        """
        pool = Pool()
        User = pool.get('galatea.user')
        Product = pool.get('product.product')
        Shop = pool.get('sale.shop')
        SaleLine = pool.get('sale.line')

        if user and not isinstance(user, User):
            user = User(user)

        # not filter by shop. Update all current carts
        domain = [
            ('sale', '=', None),
            ]
        if user: # login user. Filter sid or user
            domain.append(['OR',
                ('sid', '=', session.sid),
                ('galatea_user', '=', user),
                ])
        else: # anonymous user. Filter sid
            domain.append(
                ('sid', '=', session.sid),
                )
        lines = SaleLine.search(domain)

        context = {}
        if user:
            context['customer'] = user.party.id
        if user and user.party.sale_price_list:
            context['price_list'] = user.party.sale_price_list.id
        else:
            shop = Transaction().context.get('shop')
            if shop:
                shop = Shop(shop)
                context['price_list'] = shop.price_list.id

        to_save = []
        with Transaction().set_context(context):
            for line in lines:
                prices = Product.get_sale_price([line.product], line.quantity or 0)
                price = prices[line.product.id]

                if hasattr(SaleLine, 'gross_unit_price'):
                    line.gross_unit_price = price
                    line.update_prices()
                else:
                    line.unit_price = price

                to_save.append(line)

        if to_save:
            SaleLine.save(to_save)

        super(GalateaUser, cls).signal_login(user, session, website)
