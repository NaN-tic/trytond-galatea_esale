
# This file is part of Tryton.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from trytond.modules.company.tests import CompanyTestMixin
from trytond.tests.test_tryton import ModuleTestCase


class GalateaEsaleCompanyTestMixin(CompanyTestMixin):

    @property
    def _skip_company_rule(self):
        return super()._skip_company_rule | {
            ('galatea.website', 'company'),
            }


class GalateaEsaleTestCase(GalateaEsaleCompanyTestMixin, ModuleTestCase):
    'Test GalateaEsale module'
    module = 'galatea_esale'
    extras = ['product_esale_categories', 'sale_pos']

del ModuleTestCase
