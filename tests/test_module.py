
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.

from trytond.modules.company.tests import CompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase


class GalateaEsaleTestCase(CompanyTestMixin, ModuleTestCase):
    'Test GalateaEsale module'
    module = 'galatea_esale'
    extras = ['product_esale_categories', 'sale_pos']


del ModuleTestCase
