# -*- coding: utf-8 -*-

from openerp import models, fields


class country(models.Model):
        _inherit = 'res.country'
        afip_code = fields.Char(
            'AFIP code',
            size=64,
            help='Codigo oficial del AFIP.')


class country_state(models.Model):
        _inherit = 'res.country.state'

        afip_code = fields.Char(
            'AFIP code',
            size=64,
            help='Codigo oficial del AFIP.')

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
