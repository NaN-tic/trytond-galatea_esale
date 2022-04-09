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

    @classmethod
    def __setup__(cls):
        Category = Pool().get('product.category')

        super(GalateaWebSite, cls).__setup__()

        if hasattr(Category, 'esale_active'):
            cls.esale_category_menu = fields.Many2One('product.category',
                'Catalog Category Menu', domain=[
                    ('esale_active', '=', True),
                ], context={
                    'company': Eval('company'),
                }, depends=['company'],
                help='Main menu of catalog category')


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
        Sale = pool.get('sale.sale')
        SaleLine = pool.get('sale.line')

        if user and not isinstance(user, User):
            user = User(user)

        context = {}
        if user:
            context['customer'] = user.party.id
        if user and user.party.sale_price_list:
            context['price_list'] = user.party.sale_price_list.id
        else:
            shop = Transaction().context.get('shop')
            if shop:
                shop = Shop(shop)
                context['price_list'] = (shop.price_list.id
                    if shop.price_list else None)

        to_save = []
        with Transaction().set_context(**context):
            default_values = Sale.default_get(Sale._fields.keys(),
                with_rec_name=False)
            sale = Sale(**default_values)
            sale.party = user.party
            sale.price_list = context.get('price_list', None)

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

            for line in lines:
                # sure reload the product according to context (taxes)...
                product = Product(line.product.id)
                line.product = product
                line.sale = sale
                if not line.party:
                    line.party = user.party
                line.galatea_user = user
                line.sid = None

                prices = Product.get_sale_price([product], line.quantity or 0)
                price = prices.get(product.id)
                if price:
                    if hasattr(SaleLine, 'gross_unit_price'):
                        line.gross_unit_price = price
                        line.update_prices()
                    else:
                        line.unit_price = price

                    # recalculate line data (taxes,...)
                    line.on_change_product()

                # set sale to None
                line.sale = None
                to_save.append(line)

        if to_save:
            SaleLine.save(to_save)

        super(GalateaUser, cls).signal_login(user, session, website)
