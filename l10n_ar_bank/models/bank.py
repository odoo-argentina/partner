# -*- coding: utf-8 -*-
from openerp import fields, models, api
from openerp.exceptions import ValidationError


class Bank(models.Model):
    _inherit = 'res.bank'

    bcra_code = fields.Char(
        'BCRA Code',
        size=8,
        help="Code assigned by BCRA")
    vat = fields.Char(
        'VAT',
        size=32,
        help="Value Added Tax number.")


class partner_bank(models.Model):
    _name = 'res.partner.bank'
    _inherit = 'res.partner.bank'

    @api.multi
    def is_valid_ar_acc_number(self):
        self.ensure_one()

        cbu = self.acc_number

        if type(cbu) == int:
            cbu = "%022d" % cbu
        cbu = cbu.strip().replace('-', '').replace(' ', '')
        if len(cbu) != 22:
            return False
        s1 = sum(int(a)*b for a, b in zip(cbu[0:7], (7, 1, 3, 9, 7, 1, 3)))
        d1 = (10 - s1) % 10
        if d1 != int(cbu[7]):
            return False
        s2 = sum(int(a)*b
                 for a, b in zip(cbu[8:-1],
                                 (3, 9, 7, 1, 3, 9, 7, 1, 3, 9, 7, 1, 3)))
        d2 = (10 - s2) % 10
        if d2 != int(cbu[-1]):
            return False

        return True

    @api.onchange('acc_number')
    def set_bank_from_ar_acc_number(self):
        if self.acc_number and \
                self.partner_id.country_id.code == 'AR' and \
                self.is_valid_ar_acc_number() and \
                not self.bank_id:
            bank_code = int(self.acc_number[:3])
            self.bank_id = self.bank_id.search(
                [['bcra_code', '=', "%05i" % bank_code]],
                limit=1
            )

    @api.constrains('acc_number', 'bank_id.country')
    def check_ar_acc_number(self):
        if self.acc_number and self.bank_id and \
                self.bank_id.country.code == 'AR' and \
                not self.is_valid_ar_acc_number():
            raise ValidationError("Account Number is an invalid CBU.")

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
