# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from simpleeval import simple_eval
from trytond.pool import Pool, PoolMeta
from trytond.model import ModelView, ModelSQL, fields
from trytond.transaction import Transaction
from trytond.pyson import Eval
from trytond.tools import decistmt

__all__ = ['GalateaWebSite', 'GalateaUser', 'GalateaEsaleRule']


class GalateaWebSite:
    __metaclass__ = PoolMeta
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
    rules = fields.One2Many('galatea.esale.rule', 'website', 'Rules')

    @staticmethod
    def default_esale_stock_qty():
        return 'quantity'


class GalateaUser:
    __metaclass__ = PoolMeta
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


class GalateaEsaleRule(ModelSQL, ModelView):
    'Galatea eSale Rule'
    __name__ = "galatea.esale.rule"
    website = fields.Many2One('galatea.website', 'Website', required=True, select=True)
    sequence = fields.Integer('Sequence', required=True)
    formula = fields.Char('Formula', required=True,
        help=('Python expression that will be evaluated. Eg:\n'
            'getattr(record, "total_amount") > 0'))
    sale_invoice_method = fields.Selection(
        'get_sale_invoice_methods', "Sale Invoice Method")
    sale_shipment_method = fields.Selection(
        'get_sale_shipment_methods', "Sale Shipment Method")
    sale_state = fields.Selection(
        'get_sale_state', "Sale State")
    payment_type = fields.Many2One('account.payment.type', 'Payment type')
    active = fields.Boolean('Active', select=True)
    message = fields.Char('Message', translate=True,
        help='Message that show when apply the rule')

    @classmethod
    def __setup__(cls):
        super(GalateaEsaleRule, cls).__setup__()
        cls._order.insert(0, ('website', 'ASC'))
        cls._order.insert(0, ('sequence', 'ASC'))

    def get_sale_selection(field_name):
        @classmethod
        def func(cls):
            pool = Pool()
            Sale = pool.get('sale.sale')
            return [(None, '')] + Sale.fields_get([field_name])[field_name]['selection']
        return func

    get_sale_invoice_methods = get_sale_selection('invoice_method')
    get_sale_shipment_methods = get_sale_selection('shipment_method')
    get_sale_state = get_sale_selection('state')

    @classmethod
    def default_website(cls):
        Website = Pool().get('galatea.website')
        websites = Website.search([0])
        if len(websites) == 1:
            return websites[0].id

    @staticmethod
    def default_active():
        return True

    @staticmethod
    def default_sequence():
        return 0

    @classmethod
    def get_context_formula(cls, record):
        return {
            'names': {
                'record': record,
            },
            'functions': {
                'getattr': getattr,
                'setattr': setattr,
                'hasattr': hasattr,
                'Decimal': Decimal,
                'round': round,
                },
            }

    def set_record_rule(self, record):
        if self.sale_invoice_method:
            record.invoice_method = self.sale_invoice_method
        if self.sale_shipment_method:
            record.shipment_method = self.sale_shipment_method
        if self.payment_type:
            record.payment_type = self.payment_type
        if self.sale_state:
            record.state = self.sale_state
        if self.message:
            record.comment = self.message
        return record

    @classmethod
    def compute_rule(cls, website, record):
        "Compute rule based on formula"
        context = cls.get_context_formula(record)
        for rule in website.rules:
            if simple_eval(decistmt(rule.formula), **context):
                return rule.set_record_rule(record)
        return record
