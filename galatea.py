# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import Pool, PoolMeta
from trytond.transaction import Transaction
from trytond.pyson import Eval

__all__ = ['GalateaWebSite', 'GalateaUser']
__metaclass__ = PoolMeta


class GalateaWebSite:
    __name__ = "galatea.website"
    esale_menu = fields.Many2One('esale.catalog.menu', 'Main Menu', required=True,
        help='Main menu product catalog')
    esale_stock = fields.Boolean('Stock',
        help='Manage Stock')
    esale_stock_qty = fields.Selection([
        ('quantity', 'Quantity'),
        ('forecast_quantity', 'Forecast Quantity'),
        ], 'Quantity Stock', states={
            'invisible': ~Eval('esale_stock', True),
        },
        help='Manage Stock is Product Quantity or Product Forecast Quantity')

    @staticmethod
    def default_esale_stock_qty():
        return 'quantity'


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

    @classmethod
    def signal_login(cls, user, session=None, website=None):
        """Flask signal to login
        Update cart prices when user login
        """
        pool = Pool()
        SaleCart = pool.get('sale.cart')
        User = pool.get('galatea.user')
        Shop = pool.get('sale.shop')
        Product = pool.get('product.product')
        
        user = User(user)

        # not filter by shop. Update all current carts
        domain = [
            ('state', '=', 'draft'),
            ]
        if session: # login user. Filter sid or user
            domain.append(['OR', 
                ('sid', '=', session),
                ('galatea_user', '=', user),
                ])
        else: # anonymous user. Filter user
            domain.append(
                ('sid', '=', session),
                )
        carts = SaleCart.search(domain)

        context = {}
        context['customer'] = user.party.id
        if user.party.sale_price_list:
            context['price_list'] = user.party.sale_price_list.id
        else:
            shop = Transaction().context.get('shop')
            if shop:
                shop = Shop(shop)
                context['price_list'] = shop.price_list.id

        with Transaction().set_context(context):
            for cart in carts:
                price = Product.get_sale_price([cart.product],
                            cart.quantity)[cart.product.id]
                cart.unit_price = price
                cart.save() #TODO 3.6 save multiples records

        super(GalateaUser, cls).signal_login(user, session, website)
