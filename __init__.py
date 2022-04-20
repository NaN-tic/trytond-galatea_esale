# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.pool import Pool
from . import galatea
from . import menu
from . import sale
from . import product
from . import payment_type


def register():
    Pool.register(
        menu.CatalogMenu,
        galatea.GalateaWebSite,
        galatea.GalateaUser,
        payment_type.PaymentType,
        sale.Sale,
        sale.SaleLine,
        product.Category,
        product.ProductCategoryGalateaWebsite,
        product.Template,
        product.Product,
        module='galatea_esale', type_='model')
