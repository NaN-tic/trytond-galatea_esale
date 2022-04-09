# This file is part of the galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains the full
# copyright notices and license terms.
import unittest
import trytond.tests.test_tryton
from trytond.tests.test_tryton import ModuleTestCase
from trytond.modules.company.tests import CompanyTestMixin


class GalateaEsaleTestCase(CompanyTestMixin, ModuleTestCase):
    'Test Galatea Esale module'
    module = 'galatea_esale'


def suite():
    suite = trytond.tests.test_tryton.suite()
    suite.addTests(unittest.TestLoader().loadTestsFromTestCase(
        GalateaEsaleTestCase))
    return suite
