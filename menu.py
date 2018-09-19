# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta

__all__ = ['CatalogMenu']


class CatalogMenu(metaclass=PoolMeta):
    __name__ = 'esale.catalog.menu'
    website = fields.Many2One('galatea.website', 'Website')

    @fields.depends('parent')
    def on_change_with_website(self):
        """Add website from parent"""
        if self.parent and self.parent.website:
            return self.parent.website.id
        return None
