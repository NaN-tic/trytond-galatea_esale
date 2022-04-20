# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields, ModelSQL
from trytond.pool import Pool, PoolMeta
from trytond.pyson import Eval
from trytond.transaction import Transaction
from trytond.config import config as config_

__all__ = ['Category', 'ProductCategoryGalateaWebsite', 'Template', 'Product']

DIGITS = config_.getint('product', 'price_decimal', default=4)


class Category(metaclass=PoolMeta):
    __name__ = "product.category"

    @classmethod
    def __setup__(cls):
        super(Category, cls).__setup__()
        if hasattr(cls, 'esale_active'):
            cls.websites = fields.Many2Many('product.category-galatea.website',
                'category', 'website', "Websites")

    @classmethod
    def __register__(cls, module_name):
        table = cls.__table_handler__(module_name)

        has_website = False
        if hasattr(cls, 'esale_active'):
            if table.column_exist('website'):
                has_website = True

        super(Category, cls).__register__(module_name)
        table = cls.__table_handler__(module_name)

        if has_website:
            Website = Pool().get('galatea.website')

            websites = Website.search([])

            query = 'select id from product_category where website is not null'
            cursor = Transaction().connection.cursor()
            cursor.execute(query)
            ids = [id[0] for id in cursor.fetchall()]
            if ids and websites:
                categories = cls.browse(ids)
                cls.write(categories, {'websites': [
                    ('add', [w.id for w in websites])]})
            table.drop_column('website')


class ProductCategoryGalateaWebsite(ModelSQL):
    'Product Category - Galatea Website'
    __name__ = 'product.category-galatea.website'
    category = fields.Many2One('product.category', "Category",
        ondelete='CASCADE', required=True, select=True)
    website = fields.Many2One('galatea.website', "Website",
        ondelete='CASCADE', required=True, select=True)


class Template(metaclass=PoolMeta):
    __name__ = 'product.template'
    esale_new = fields.Boolean('New', help='Icon New product')
    esale_hot = fields.Boolean('Hot', help='Icon Hot product')
    esale_menus_by_website = fields.Function(fields.Many2Many(
        'esale.catalog.menu', None, None, 'Menus by Website'),
        'get_esale_menus_by_website')
    esale_global_price = fields.Numeric('eSale Global Price',
        digits=(16, DIGITS),
        states={
            'readonly': ~Eval('active', True),
            'required': Eval('esale_available', False),
            },
        depends=['active', 'esale_available'])

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

    @fields.depends('list_price')
    def on_change_with_esale_global_price(self, name=None):
        if self.list_price:
            return self.list_price


class Product(metaclass=PoolMeta):
    __name__ = 'product.product'
    add_cart = fields.Boolean('Add Cart', states={
            'readonly': ~Eval('active', True),
            }, depends=['active'],
            help='Available to add cart')

    @staticmethod
    def default_add_cart():
        return True
