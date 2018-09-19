# This file is part galatea_esale module for Tryton.
# The COPYRIGHT file at the top level of this repository contains
# the full copyright notices and license terms.
from trytond.model import fields
from trytond.pool import PoolMeta
from trytond.pyson import Eval

__all__ = ['PaymentType']


class PaymentType(metaclass=PoolMeta):
    __name__ = 'account.payment.type'
    esale_payment = fields.Boolean('Virtual Payment')
    esale_code = fields.Char('Code App Payment', states={
            'required': Eval('esale_payment', False),
            },
        depends=['esale_payment'])
