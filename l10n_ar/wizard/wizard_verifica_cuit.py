
import wizard
import math
from osv import osv
from tools.misc import UpdateableStr
import pooler
import string

def _get_cuit (cuit):
	cstr = str (cuit)
        salt=str (5432765432)
        n=0
        sum=0
	if not cuit.isdigit:
		return 'CUIT no numeral'
        
	if (len (cuit) <> 11):
		return  "CUIT debe tener 11 digitos"
	while (n < 10):
		sum = sum + int (salt[n]) * int (cstr[n])
                n=n+1
        op1 = sum % 11
        op2 = 11 - op1
        codigo_verificador = op2
        if ( op2 == 11 or op2 == 10):
                if ( op2 == 11 ):
                        codigo_verificador = 0
                else:
                        codigo_verificador = 9
        if ( codigo_verificador == int (cstr[10]) ):
                return 'OK'                
        else:
                return 'Error en CUIT'


_check_arch = UpdateableStr()
_check_fields = {}

def _verifica_cuit(self, cr, uid, data, context):
	partner_table=pooler.get_pool(cr.dbname).get('res.partner')
	partners = partner_table.browse(cr, uid, data['ids'])
	_check_arch_lst=['<?xml version="1.0"?>', '<form string="Verifica CUIT">', '<label string="CUIT" />','<label string="Status" />']
	for partner in partners:
		if partner['vat']:
			_check_arch_lst.append('<label string=""/>')
			_check_arch_lst.append('<label string=""/>')
			_check_arch_lst.append('<label string="%s" />' % partner['vat']);
			cod_ver=_get_cuit(partner['vat'])
			_check_arch_lst.append('<label string="%s"/>' % cod_ver)
	_check_arch_lst.append('</form>')
	_check_arch.string = '\n'.join(_check_arch_lst)
	return {}


class wiz_ean_check(wizard.interface):
	states = {
		'init': {
			'actions': [_verifica_cuit],
			'result': {
				'type': 'form',
				'arch': _check_arch,
				'fields': _check_fields,
				'state': [('end','OK')]
			}
		},
		
	}

wiz_ean_check('l10n_ar.verifica_cuit')
