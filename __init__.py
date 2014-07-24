#This file is part galatea_esale module for Tryton.
#The COPYRIGHT file at the top level of this repository contains 
#the full copyright notices and license terms.
from trytond.pool import Pool
from .galatea import *
from .sale_cart import *
from .shop import *
from .product import *
from .payment_type import *

def register():
    Pool.register(
        GalateaWebSite,
        GalateaUser,
        PaymentType,
        SaleCart,
        SaleShop,
        Template,
        module='galatea_esale', type_='model')
