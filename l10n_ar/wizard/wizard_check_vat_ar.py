# -*- coding: utf-8 -*-
##############################################################################
#
#    Copyright (C) 2008-2011  Luis Falcon
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
#
##############################################################################

import wizard
import math
from osv import osv
from tools.misc import UpdateableStr
import pooler
import string


def _get_vat_ar(vat):
    '''
    Check VAT (CUIT) for Argentina - Thymbra
    '''
    cstr = str(vat)
    salt = str(5432765432)
    n = 0
    sum = 0

    if not vat.isdigit:
        return 'CUIT no numeral'

    if (len(vat) != 11):
        return 'CUIT debe tener 11 digitos'

    while (n < 10):
        sum = sum + int(salt[n]) * int(cstr[n])
        n = n + 1

    op1 = sum % 11
    op2 = 11 - op1

    code_verifier = op2

    if (op2 == 11 or op2 == 10):
        if (op2 == 11):
            code_verifier = 0
        else:
            code_verifier = 9

    if (code_verifier == int(cstr[10])):
        return 'OK'
    else:
        return 'Error en CUIT'


_check_arch = UpdateableStr()
_check_fields = {}


def _check_vat_ar(self, cr, uid, data, context):
    partner_table = pooler.get_pool(cr.dbname).get('res.partner')
    partners = partner_table.browse(cr, uid, data['ids'])
    _check_arch_lst = [
        '<?xml version="1.0"?>',
        '<form string="Verifica CUIT">',
        '<label string="CUIT"/>',
        '<label string="Status"/>',
    ]
    for partner in partners:
        if partner['vat']:
            _check_arch_lst.append('<label string=""/>')
            _check_arch_lst.append('<label string=""/>')
            _check_arch_lst.append('<label string="%s"/>' % partner['vat'])
            cod_ver = _get_vat_ar(partner['vat'])
            _check_arch_lst.append('<label string="%s"/>' % cod_ver)
    _check_arch_lst.append('</form>')
    _check_arch.string = '\n'.join(_check_arch_lst)
    return {}


class wiz_ean_check(wizard.interface):
    states = {
        'init': {
            'actions': [
                _check_vat_ar,
            ],
            'result': {
                'type': 'form',
                'arch': _check_arch,
                'fields': _check_fields,
                'state': [
                    ('end', 'OK'),
                ]
            }
        },
    }

wiz_ean_check('l10n_ar.check_vat_ar')
