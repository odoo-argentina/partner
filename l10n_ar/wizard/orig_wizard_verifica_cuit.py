import wizard
from osv import osv

cuit_form = """<?xml version="1.0"?>
<form title="Verificador de CUIT">
    <field name="cuit_number"/>
    <field name="codigo_actual"/>
    <newline/>
    <field name="codigo_computado"/>
</form>"""

cuit_fields = {
    'cuit_number': {'string': 'Num. de CUIT', 'type':'char', 'readonly':True},
    'codigo_actual': {'string': 'Cod. Ver. actual', 'type':'integer', 'readonly':True},
    'codigo_computado': {'string': 'Cod. Ver. computado', 'type':'integer', 'readonly':True},
}

def _verifica_cuit (self, cr, uid, data, context):
        cstr = str (cuit)
        salt=str (5432765432)
        n=0
        sum=0
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
                        codigo=verificarod = 9
        if ( codigo_verificador == int (cstr[10]) ):
                return 0                
        else:
                return 1 


class wiz_verifica_cuit(wizard.interface):
	states = {
		'init': {
			'actions': [_verifica_cuit],
			'result': {
				'type': 'form',
				'arch': cuit_form,
				'fields': cuit_fields,
				'state': (('end', 'Ignorar'), ('correct', 'Corregir'))
			}
		},
		'correct' : {
			'actions': [_verifica_cuit],
			'result': {
				'type': 'state',
				'state': 'end'
			}
		}
	}

wiz_verifica_cuit('l10n_ar.verifica_cuit')
