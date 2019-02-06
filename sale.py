# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from decimal import Decimal
from trytond.pool import Pool, PoolMeta
from trytond.model import fields
from trytond.pyson import Eval, Not, Bool, And
from trytond.transaction import Transaction

__all__ = ['Sale', 'SaleLine']


class Sale(metaclass=PoolMeta):
    __name__ = 'sale.sale'
    galatea_user = fields.Many2One('galatea.user', 'Galatea User',
         readonly=True)

    @classmethod
    def get_esale_carriers(cls, shop, party=None, untaxed=0, tax=0, total=0, payment=None):
        '''Available eSale Carriers'''
        PaymentType = Pool().get('account.payment.type')

        sale = cls()
        sale.party = party
        sale.untaxed_amount = untaxed
        sale.tax_amount = tax
        sale.total_amount = total
        if isinstance(payment, int):
            sale.payment_type = PaymentType(payment)
        else:
            sale.payment_type = payment

        context = {}
        context['record'] = sale # Eval by "carrier formula" require "record"
        decimals = "%0."+str(shop.currency.digits)+"f" # "%0.2f" euro

        carriers = []
        for ecarrier in shop.esale_carriers:
            carrier = ecarrier.carrier
            context['carrier'] = carrier
            with Transaction().set_context(context):
                carrier_price = carrier.get_sale_price() # return price, currency
            price = carrier_price[0]
            price_w_tax = carrier.get_sale_price_w_tax(price, party=party)
            carrier.fullname = '%s (+%s %s)' % (
                    carrier.rec_name,
                    Decimal(decimals % price_w_tax),
                    shop.currency.code)
            carrier.price = Decimal(decimals % price)
            carrier.price_w_tax = Decimal(decimals % price_w_tax)
            carriers.append(carrier)
        return carriers

    def set_esale_sale(self, data):
        '''Overwrite this method to add more fields in sale object from request.form.data'''
        return self

    def get_esale_lines(self):
        '''Return sale lines without shipment cost lines'''
        return [l for l in self.lines if (
            l.product and l.product.esale_available and (
                l.shipment_cost is None or l.shipment_cost == 0))]

    def _get_extra_lines(self):
        """
        Return extra lines to will be created.
        This method will be overwritten by other modules.

        """
        return []


class SaleLine(metaclass=PoolMeta):
    __name__ = 'sale.line'
    sid = fields.Char('Session')
    galatea_user = fields.Many2One('galatea.user', 'Galatea User', readonly=True)
    product_id = fields.Function(fields.Integer('Product ID'), 'get_product_id')
    template_id = fields.Function(fields.Integer('Template ID'), 'get_template_id')
    shop = fields.Many2One('sale.shop', 'Shop', domain=[
        ('id', 'in', Eval('context', {}).get('shops', [])),
        ])

    @classmethod
    def __setup__(cls):
        super(SaleLine, cls).__setup__()
        cls.party.states['required'] = And((Not(Bool(Eval('sid')))), cls.party.states['required'])
        cls.party.depends.append('sid')

    def get_product_id(self, name):
        '''Return product ID'''
        if self.product:
            return self.product.id
        return None

    def get_template_id(self, name):
        '''Return template ID'''
        if self.product:
            return self.product.template.id
        return None

    def on_change_product(self):
        super(SaleLine, self).on_change_product()

        if not self.product:
            return

        party = self.party if hasattr(self, 'party') else None
        if party:
            # Set taxes before unit_price to have taxes in context of sale price
            taxes = []
            pattern = self._get_tax_rule_pattern()
            for tax in self.product.customer_taxes_used:
                if party.customer_tax_rule:
                    tax_ids = party.customer_tax_rule.apply(tax, pattern)
                    if tax_ids:
                        taxes.extend(tax_ids)
                    continue
                taxes.append(tax.id)
            if party.customer_tax_rule:
                tax_ids = party.customer_tax_rule.apply(None, pattern)
                if tax_ids:
                    taxes.extend(tax_ids)
            self.taxes = taxes

    @classmethod
    def copy(cls, lines, default=None):
        new_lines = [x for x in lines if x.shipment_cost is None]
        return super(SaleLine, cls).copy(new_lines, default=default)
