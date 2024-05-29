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
    def galatea_domain(cls, session):
        return []

    @classmethod
    def galatea_admin_domain(cls, session):
        return []

    @classmethod
    def _esale_carriers_sale(cls, shop, party=None, untaxed=0, tax=0, total=0,
            payment=None, address_id=None, postal_code=None, country=None):
        pool = Pool()
        PaymentType = pool.get('account.payment.type')
        Address = pool.get('party.address')
        Country = pool.get('country.country')

        sale = cls()
        sale.party = party
        sale.untaxed_amount = untaxed
        sale.tax_amount = tax
        sale.total_amount = total
        sale.payment_type = (PaymentType(payment)
            if isinstance(payment, int) else payment)

        if address_id:
            sale.shipment_address = (Address(address_id)
                if isinstance(address_id, int) else address_id)
        else:
            shipment_address = Address()
            shipment_address.postal_code = postal_code
            shipment_address.country = (Country(country)
                if isinstance(country, int) else country)
            sale.shipment_address = shipment_address
        sale.carrier = None

        return sale

    @classmethod
    def _esale_carriers_pattern(cls, party=None, address_id=None, postal_code=None,
            country=None):
        pool = Pool()
        Address = pool.get('party.address')

        pattern = {}
        if address_id and party:
            addresses = Address.search([
                ('party', '=', party),
                ('id', '=', address_id),
                ], limit=1)
            if addresses:
                address, = addresses
                postal_code = address.postal_code
                country = address.country.id if address.country else None
        if postal_code:
            pattern['shipment_postal_code'] = postal_code
        if country:
            pattern['to_country'] = country
        return pattern

    @classmethod
    def shop_esale_carriers(cls, shop, sale):
        return [ecarrier.carrier for ecarrier in shop.esale_carriers]

    @classmethod
    def get_esale_carriers(cls, shop, party=None, untaxed=0, tax=0, total=0,
            payment=None, address_id=None, postal_code=None, country=None):
        '''Available eSale Carriers'''
        pool = Pool()
        CarrierSelection = pool.get('carrier.selection')

        sale = cls._esale_carriers_sale(shop, party, untaxed, tax, total,
            payment, address_id, postal_code, country)

        available_carriers_ids = [c.id for c in sale.on_change_with_available_carriers()]
        sale.shipment_address = None

        def _values(sale):
            values = {}
            if not sale._values:
                return values
            for fname, value in sale._values._items():
                values[fname] = value
            return values

        context = {}
        context['record'] = _values(sale) # Eval by "carrier formula" require "record"
        context['record_model'] = 'sale.sale'
        decimals = "%0."+str(shop.currency.digits)+"f" # "%0.2f" euro

        pattern = cls._esale_carriers_pattern(party, address_id, postal_code, country)
        zip_carriers = CarrierSelection.get_carriers(pattern)

        carriers = []
        for carrier in cls.shop_esale_carriers(shop, sale):
            if ((carrier.id not in available_carriers_ids) or (carrier not in zip_carriers)):
                continue

            context['carrier'] = str(carrier)
            with Transaction().set_context(context):
                carrier_price = carrier.get_sale_price() # return price, currency
            price = carrier_price[0] or Decimal(0)
            price_w_tax = carrier.get_sale_price_w_tax(price, party=party)

            carriers.append({
                'carrier': carrier,
                'fullname': '%s (+%s %s)' % (carrier.rec_name,
                        Decimal(decimals % price_w_tax), shop.currency.code),
                'price': Decimal(decimals % price),
                'price_w_tax': Decimal(decimals % price_w_tax),
                })
        # sort carriers by price field
        return sorted(carriers, key=lambda k: k['price'])

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
        cls.party.depends.add('sid')

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

        if not self.product or self.taxes:
            return

        party = self.party if hasattr(self, 'party') else None
        # Set taxes before unit_price to have taxes in context of sale price
        self.taxes = self.compute_taxes(party)

    @classmethod
    def copy(cls, lines, default=None):
        new_lines = [x for x in lines if x.shipment_cost is None]
        return super(SaleLine, cls).copy(new_lines, default=default)
