# coding=utf-8

# (C) Luis Falcon - Thymbra
# GPL - GNU Public License



from osv import fields, osv

class tipo_comprobante(osv.osv):
	_name = "account.invoice"
	_inherit = "account.invoice"
	_order = "id"
	_columns = {
                'tipo_comprobante' : fields.selection([
                                ('01','01-Factura A'),
                                ('02','02-Nota de Débito A'),
                                ('03','03-Nota de Crédito A'),
                                ('04','04-Recibos A'),
                                ('05','05-Nota de Venta al Contado A'),
                                ('06','06-Factura B'),
                                ('07','07-Nota de Débito B'),
                                ('08','08-Nota de Crédito B'),
                                ('09','09-Recibos B'),
                                ('10','10-Notas de Venta al Contado B'),
                                ('39','39-Otros comprobantes A contemplados en RG 3419'),
                                ('40','40-Otros comprobantes B contemplados en RG 3419'),
                                ('60','60-Cuenta de Venta y Líquido producto A'),
                                ('61','61-Cuenta de Venta y Líquido producto B'),
                                ('63','63-Liquidación A'),
                                ('64','64-Liquidación B'),
                                ('C','C-Factura C'),
                                ('M','M-Factura M'),
                                ('E','E-Factura E'),
                                ], 'Comprobante', select=True),

	}

tipo_comprobante ()

class fechas_de_servicio(osv.osv):
	_name = "account.invoice"
	_inherit = "account.invoice"
	_columns = {
		'serv_fecha_hasta' : fields.date('Serv. hasta',help="Seleccionar fecha de fin de servicios - Sólo para empresas prestadoras de servicios"),
                'serv_fecha_desde' : fields.date('Serv. desde',help="Seleccionar fecha de inicio de servicios - Sólo para empresas prestadoras de servicios"),
		'sucursal': fields.many2one('sale.shop','Sucursal', required=True, select=True)
		   }

fechas_de_servicio ()


class condicion_iva (osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	_columns = {
                'cond_iva' : fields.selection([
                                ('01','IVA Resp. Inscripto'),
                                ('02','IVA Resp. no Inscripto'),
                                ('03','IVA no responsable'),
                                ('04','Sujeto Exento'),
                                ('05','Consumidor final'),
                                ('06','Responsable Monotributo'),
                                ('07','Sujeto no Categorizado'),
                                ('08','Importador del Exterior'),
                                ('09','Cliente del Exterior'),
                                ('10','IVA Liberado - Ley 19640'),
                                ('11','Agente de Percepción'),
                                ], 'Condición IVA', select=True),

	}

condicion_iva ()

class condicion_iibb (osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	_columns = {
                'cond_iibb' : fields.selection([
                                ('01','Contribuyente Local'),
                                ('02','Convenio Multilateral'),
                                ('03','Exento'),
                                ], 'Condición IIBB', select=True),

	}

condicion_iibb ()

class presta_servicios (osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	_columns = {
		'servicios' : fields.boolean('Servicios', help="Marcar si la empresa ofrece servicios"),
		
	}

presta_servicios ()

class numero_iibb (osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	_columns = {
		'iibb' : fields.char('IIBB', size=15, help="Número de Ingresos Brutos"),
	}

numero_iibb ()

# Sucursal encargada en emitir la factura electrónica

class sucursal_emisora (osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	_columns = {
		'sucursal_emisora' : fields.many2one('sale.shop','Sucursal Emisora', help="Sucursal encargada en emitir la factura electrónica"), 
	}

sucursal_emisora ()

class numero_cuit_canal (osv.osv):
	_name = "res.partner"
	_inherit = "res.partner"
	_columns = {
		'cuit_canal' : fields.char('CUIT Canal', size=15, help="CUIT de la empresa canal para la AFIP"),
	}

numero_cuit_canal ()

# campo para el codigo de sucursal

class shop_code(osv.osv):
       _name = "sale.shop"
       _inherit = "sale.shop"
       _columns = {
#	       'name': fields.integer('sucursal',required=True, select=True, help='Código numérico de la sucursal (ej, 1)'),
               'shop_desc': fields.char('Descripción', size=50, select=True, help='Descripción de la sucursal'),
               }

shop_code ()

# campo para el codigo de moneda de la AFIP

class shop_code(osv.osv):
       _name = "res.currency"
       _inherit = "res.currency"
       _columns = {
	       'afip': fields.char('AFIP',size=10, help='Código específico de la AFIP para la moneda'),
               }

shop_code ()

# Tabla que contiene los tipos de documentos en Argentina

class documento_identidad(osv.osv):
	_name = "account.invoice.dt"
	_columns = {
		'name': fields.char ('Código',size=2,select=True, help='Codigo identificador'),
		'desc': fields.char ('Descripción',size=30, select=True, help='Descripción del documento'),
		}

documento_identidad ()

# Tipo de documento de Identidad en la Factura

class tipo_de_documento(osv.osv):
	_name = "account.invoice"
	_inherit = "account.invoice"
	_columns = {
		'id_type': fields.many2one('account.invoice.dt','ID del Comprador', select=True,required=True),
		   }

tipo_de_documento ()


class invoice_extended (osv.osv):
	_inherit="account.invoice"
        def action_number(self, cr, uid, ids, *args):
                cr.execute('SELECT id, type, number, move_id, partner_id, tipo_comprobante FROM account_invoice WHERE id IN ('+','.join(map(str,ids))+')')
                for (id, invtype, number, move_id, partner_id, tipo_comprobante) in cr.fetchall():

                        if not number:
				if (invtype == "out_invoice"):
	                                number = self.pool.get('ir.sequence').get(cr, uid, 'account.invoice.'+invtype+'_'+tipo_comprobante)
				else:
	                              	number = self.pool.get('ir.sequence').get(cr, uid, 'account.invoice.'+invtype)
                                cr.execute('UPDATE account_invoice SET number=%s WHERE id=%s', (number, id))
                                cr.execute('UPDATE account_move_line SET ref=%s WHERE move_id=%s and ref is null', (number, move_id))
                return True


invoice_extended ()

