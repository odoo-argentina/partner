# coding: utf-8

# Están muchos valores de importe con valor absoluto, puesto que el CAE en AFIP no acepta valores negativos.


from osv import fields,osv
import pooler
import base64
import string
import StringIO
from xml.dom.minidom import getDOMImplementation
import time
import math

import sys

class genera_formulario_cae (osv.osv_memory):


	def generar_archivo (self, cr, uid, ids, context={}):

		temp_buffer = StringIO.StringIO()




	#	Empezamos a generar el documento XML
	#	doc = Nombre del documento XML
	#	lote_comprobante = root element con toda la informacion requerida

		impl = getDOMImplementation()
		doc = impl.createDocument(None, "lote_comprobantes", None)
		lote_comprobantes = doc.documentElement

	#	Esta linea es sólo para usar con INTERFACTURAS	
		lote_comprobantes.setAttributeNS (None, "xmlns","http://lote.schemas.cfe.ib.com.ar/")

		invoice_obj = self.pool.get('account.invoice')	
		inv_ids = context.get ('active_ids')	
		invoices = invoice_obj.browse(cr, uid, inv_ids)


		self.genera_cabecera_lote (invoices,cr, doc, lote_comprobantes,temp_buffer)

		for invoice in invoices:
			comprobante = doc.createElement ("comprobante")
			lote_comprobantes.appendChild (comprobante)

	
			self.genera_cuerpo_comprobante (invoice,cr, doc,lote_comprobantes, comprobante, temp_buffer)
		
			nro_linea=0		

			# DETALLE  -- En Lineas de facturacion (debemos calcular el numero de lineas en este punto )

			detalle = doc.createElement ("detalle")
			comprobante.appendChild (detalle)

			for lineafact in invoice.invoice_line:
			
				nro_linea=nro_linea+1

				self.genera_detalle_factura (lineafact,cr, doc,lote_comprobantes, comprobante, detalle, nro_linea, temp_buffer)
							 
			self.genera_resumen_factura (invoice,cr, doc,lote_comprobantes, comprobante, temp_buffer)
				
	# Cambiamos la codificacion del documento a ISO-8859-1, que parece que es la que usa hoy AFIP

		temp_buffer.write (doc.toxml("ISO-8859-1"))
			
		try:
			contenido_buffer = base64.encodestring(temp_buffer.getvalue())			
			temp_buffer.close()

		except IOError, e:
			raise  osv.except_osv(_('UserError'),_('No se pudo grabar el archivo:\n'+nombre_archivo+'!'))


		return self.write(cr, uid, ids, {'archivo_destino':contenido_buffer, 'nombre':'cae.xml'}, context=context)
	 



	# Traduce el numero codigo standard de provincia al codigo de la AFIP
	def map_provincia_id (self,codigo):
		afip_code = {'C':1,'B':2,'K':3,'X':4,'W':5,'H':6,'U':7,'E':8,'P':9,'Y':10,'L':11,'F':12,'M':13,'N':14,'Q':15,'R':16,'A':17,'J':18,'D':19,'Z':20,'S':21,'G':22,'V':23,'T':24}	

		return (afip_code [codigo])

	# Selecciona la direccion que aparece en el documento de la factura.
	# En el caso de la dirección de la empresa, seleccionaremos la dirección predeterminada (default)

	def get_partner_address (self,partneraddrid, partner, cr):
		sql='select street, street2, city, state_id, zip, phone, email from res_partner_address where id=%s' % str(partneraddrid)
		if partner == 'empresa':
			sql='select street, street2, city, state_id, zip, phone, email from res_partner_address where type=\'default\' and partner_id=%s' % str(partneraddrid)
		cr.execute(sql)
		direccion = cr.fetchone()
		sql = 'select code from res_country_state where id=%s' % str(direccion[3])
		cr.execute(sql)
		provincia = cr.fetchone()
		codigo_provincia = provincia[0]
		codigo_afip =  self.map_provincia_id (codigo_provincia)
	#	Pasamos de tuple a list
		b=[]
		for i in direccion:
			b.append(i)
		b[3] = codigo_afip
		return (b)


	def get_iibb (self,partner_id,cr):
		sql='select iibb from res_partner where id=%s' % partner_id
		cr.execute(sql)
		iibb = cr.fetchone()
		return (str(iibb[0]))

	def get_razon_social (self,partner_id,cr):
		sql='select name from res_partner where id=%s' % partner_id
		cr.execute(sql)
		razon_social = cr.fetchone()
		return (str(razon_social[0]))

	def get_condicion_iibb (self,partner_id,cr):
		sql='select cond_iibb from res_partner where id=%s' % partner_id
		cr.execute(sql)
		cond_iibb = cr.fetchone()
		return (str(cond_iibb[0]))

	def get_condicion_iva (self,partner_id,cr):
		sql='select cond_iva from res_partner where id=%s' % partner_id
		cr.execute(sql)
		cond_iva = cr.fetchone()
		return (str(cond_iva[0]))

	def code_date (self,fecha):
		fecha1 = time.strptime (fecha,"%Y-%m-%d")
		return (time.strftime ("%Y%m%d", fecha1))

	def get_cuit_empresa (self,partner_id,cr):
		sql='select vat from res_partner where id=%s' % partner_id
		cr.execute(sql)
		cuit_empresa = cr.fetchone()
		return (str(cuit_empresa[0]))

	def get_address_id (self,invoice_id,cr):
		sql='select address_invoice_id from account_invoice where id=%s' % str(invoice_id)
		cr.execute(sql)
		address_id = cr.fetchone()
		return (address_id[0])

	# Extraemos el ID de empresa vendedora en la factura (que puede o no ser el mismo que mi compañia)

	def get_vendor_id (self,invoice_id,cr):
		sql='select company_id from account_invoice where id=%s' % str(invoice_id)
		cr.execute(sql)
		vendor_id = cr.fetchone()
		return (vendor_id[0])


	def get_cuit_canal(self,partner_id,cr):
		sql='select cuit_canal from res_partner where id=%s' % partner_id
		cr.execute(sql)
		cuit_canal = cr.fetchone()
		return (str(cuit_canal[0]))

	def get_sucursal_emisora(self,partner_id,cr):
		sql='select sucursal_emisora from res_partner where id=%s' % partner_id
		cr.execute(sql)
		sucursal_emisora = cr.fetchone()
		return (str(sucursal_emisora[0]))

	def get_rubro (self,partner_id,cr):
		sql='select servicios from res_partner where id=%s' % partner_id
		cr.execute(sql)
		brinda_servicios = 0
		rubro = cr.fetchone()
		if rubro[0]:
			brinda_servicios=1
		return (str (brinda_servicios))

	def mypartner_id (self,inv_id,cr):
		sql='select partner_id from account_invoice where id=%s' % str(inv_id)
		cr.execute(sql)
		mypartnerid = cr.fetchone()
		return (str(mypartnerid[0]))


	def mycompany_id (self,cr):
		sql='select partner_id from res_company'
		cr.execute(sql)
		myid = cr.fetchone()
		return (str (myid[0]))



	def genera_cabecera_lote (self, invoices,cr, doc,lote_comprobantes, temp_buffer):

	#	Numero unico ( fecha + hora )
		fecha_actual = time.localtime ()
		numero_lote = time.strftime ("%Y%m%d%H%M%S", fecha_actual)
		fecha_lote = time.strftime ("%Y%m%d %H%M%S", fecha_actual)
	
		numero_de_comprobantes = str (len (invoices))

		myid = self.mycompany_id (cr)


		cuit_del_canal = self.get_cuit_canal(myid,cr)

	
	# CABECERA

		cabecera_lote = doc.createElement ("cabecera_lote")
		lote_comprobantes.appendChild (cabecera_lote)

		id_lote = doc.createElement ("id_lote")
		cabecera_lote.appendChild (id_lote)
		valor = doc.createTextNode(numero_lote)
		id_lote.appendChild (valor)

		cuit_canal = doc.createElement ("cuit_canal")
		cabecera_lote.appendChild (cuit_canal)
		valor = doc.createTextNode(cuit_del_canal)
		cuit_canal.appendChild (valor)

		cuit_vendedor = doc.createElement ("cuit_vendedor")
		cabecera_lote.appendChild (cuit_vendedor)
		valor = doc.createTextNode (self.get_cuit_empresa(myid,cr))
		cuit_vendedor.appendChild (valor)

		cantidad_reg = doc.createElement ("cantidad_reg")
		cabecera_lote.appendChild (cantidad_reg)
		valor = doc.createTextNode (numero_de_comprobantes)
		cantidad_reg.appendChild (valor)

		presta_serv = doc.createElement ("presta_serv")
		cabecera_lote.appendChild (presta_serv)
		valor = doc.createTextNode (self.get_rubro(myid,cr))
		presta_serv.appendChild (valor)

		fecha_envio_lote = doc.createElement ("fecha_envio_lote")
		cabecera_lote.appendChild (fecha_envio_lote)
		valor = doc.createTextNode (str (fecha_lote))
		fecha_envio_lote.appendChild (valor)

		punto_de_venta = doc.createElement ("punto_de_venta")
		cabecera_lote.appendChild (punto_de_venta)
		valor = doc.createTextNode (str(self.get_sucursal_emisora(myid,cr)))
		punto_de_venta.appendChild (valor)
	
	
		return ()


	def genera_cuerpo_comprobante (self,invoice,cr, doc,lote_comprobantes, comprobante, temp_buffer):

		## COMPROBANTE
	
		inv_id = invoice.id
	
		mypartnerid = self.mypartner_id (inv_id,cr)
		myid = self.mycompany_id (cr)

		vendorid = self.get_vendor_id (inv_id ,cr)
	
		partneraddrid = self.get_address_id (inv_id,cr)
	
		direccion_partner = self.get_partner_address (partneraddrid,'',cr)
	
		direccion_vendedor = self.get_partner_address (vendorid,'empresa',cr)

		cabecera = doc.createElement ("cabecera")
		comprobante.appendChild (cabecera)

		informacion_comprobante = doc.createElement ("informacion_comprobante")
		cabecera.appendChild (informacion_comprobante)


		tipo_de_comprobante = doc.createElement ("tipo_de_comprobante")
		informacion_comprobante.appendChild (tipo_de_comprobante)
		valor = doc.createTextNode (str(invoice.tipo_comprobante) )
		tipo_de_comprobante.appendChild (valor)

		numero_comprobante = doc.createElement ("numero_comprobante")
		informacion_comprobante.appendChild (numero_comprobante)
		## Quitamos la parte delantera de la secuencia, delimitada por "-"

		temp_val = str(invoice.number).split('-')
		if len(temp_val) > 1:
			valor = doc.createTextNode (str(temp_val[1]))
		else:
			valor = doc.createTextNode (str(temp_val[0]))

		numero_comprobante.appendChild (valor)


		punto_de_venta = doc.createElement ("punto_de_venta")
		informacion_comprobante.appendChild (punto_de_venta)
		valor = doc.createTextNode (str(invoice.sucursal.name))
		punto_de_venta.appendChild (valor)


		fecha_emision = doc.createElement ("fecha_emision")
		informacion_comprobante.appendChild (fecha_emision)
		valor = doc.createTextNode (self.code_date (invoice.date_invoice))
		fecha_emision.appendChild (valor)

		fecha_vencimiento = doc.createElement ("fecha_vencimiento")
		informacion_comprobante.appendChild (fecha_vencimiento)
		valor = doc.createTextNode (self.code_date (invoice.date_due))
		fecha_vencimiento.appendChild (valor)

		fecha_servdesde = doc.createElement ("fecha_serv_desde")
		informacion_comprobante.appendChild (fecha_servdesde)
		valor = doc.createTextNode (self.code_date (invoice.serv_fecha_desde))
		fecha_servdesde.appendChild (valor)

		fecha_servhasta = doc.createElement ("fecha_serv_hasta")
		informacion_comprobante.appendChild (fecha_servhasta)
		valor = doc.createTextNode (self.code_date (invoice.serv_fecha_hasta))
		fecha_servhasta.appendChild (valor)

		es_detalle_encriptado = doc.createElement ("es_detalle_encriptado")
		informacion_comprobante.appendChild (es_detalle_encriptado)
		valor = doc.createTextNode ("N")
		es_detalle_encriptado.appendChild (valor)


		## Vendedor

		informacion_vendedor = doc.createElement ("informacion_vendedor")
		cabecera.appendChild (informacion_vendedor)

		razon_social = doc.createElement ("razon_social")
		informacion_vendedor.appendChild (razon_social)
		valor = doc.createTextNode (unicode (self.get_razon_social (myid, cr),'utf-8'))
		razon_social.appendChild (valor)

		cuit = doc.createElement ("cuit")
		informacion_vendedor.appendChild (cuit)
		valor = doc.createTextNode (self.get_cuit_empresa(myid,cr))
		cuit.appendChild (valor)

		condicion_IVA = doc.createElement ("condicion_IVA")
		informacion_vendedor.appendChild (condicion_IVA)
		valor = doc.createTextNode (self.get_condicion_iva (myid,cr))
		condicion_IVA.appendChild (valor)

		condicion_ingresos_brutos = doc.createElement ("condicion_ingresos_brutos")
		informacion_vendedor.appendChild (condicion_ingresos_brutos)
		valor = doc.createTextNode (self.get_condicion_iibb (myid,cr))
		condicion_ingresos_brutos.appendChild (valor)

		nro_ingresos_brutos = doc.createElement ("nro_ingresos_brutos")
		informacion_vendedor.appendChild (nro_ingresos_brutos)
		valor = doc.createTextNode (self.get_iibb(myid,cr))
		nro_ingresos_brutos.appendChild (valor)

		domicilio_calle = doc.createElement ("domicilio_calle")
		informacion_vendedor.appendChild (domicilio_calle)
		valor = doc.createTextNode (unicode (str(direccion_vendedor[0]),'utf-8'))
		domicilio_calle.appendChild (valor)

		localidad = doc.createElement ("localidad")
		informacion_vendedor.appendChild (localidad)
		valor = doc.createTextNode (unicode (str(direccion_vendedor[2]),'utf-8'))
		localidad.appendChild (valor)

		provincia = doc.createElement ("provincia")
		informacion_vendedor.appendChild (provincia)
		valor = doc.createTextNode (unicode (str(direccion_vendedor[3]),'utf-8'))
		provincia.appendChild (valor)

		cp = doc.createElement ("cp")
		informacion_vendedor.appendChild (cp)
		valor = doc.createTextNode (str(direccion_vendedor[4]))
		cp.appendChild (valor)

		email = doc.createElement ("email")
		informacion_vendedor.appendChild (email)
		valor = doc.createTextNode (str(direccion_vendedor[6]))
		email.appendChild (valor)

		telefono = doc.createElement ("telefono")
		informacion_vendedor.appendChild (telefono)
		valor = doc.createTextNode (str(direccion_vendedor[5]))
		telefono.appendChild (valor)

		## Comprador

		informacion_comprador = doc.createElement ("informacion_comprador")
		cabecera.appendChild (informacion_comprador)


		codigo_doc_identificatorio = doc.createElement ("codigo_doc_identificatorio")
		informacion_comprador.appendChild (codigo_doc_identificatorio)
		valor = doc.createTextNode (str(invoice.id_type.name))
		codigo_doc_identificatorio.appendChild (valor)

		nro_doc_identificatorio = doc.createElement ("nro_doc_identificatorio")
		informacion_comprador.appendChild (nro_doc_identificatorio)
		valor = doc.createTextNode (self.get_cuit_empresa (mypartnerid,cr))
		nro_doc_identificatorio.appendChild (valor)

		denominacion = doc.createElement ("denominacion")
		informacion_comprador.appendChild (denominacion)
		valor = doc.createTextNode (unicode (self.get_razon_social (mypartnerid,cr),'utf-8'))
		denominacion.appendChild (valor)


		domicilio_calle = doc.createElement ("domicilio_calle")
		informacion_comprador.appendChild (domicilio_calle)
		valor = doc.createTextNode (unicode (str(direccion_partner[0]),'utf-8'))
		domicilio_calle.appendChild (valor)

		localidad = doc.createElement ("localidad")
		informacion_comprador.appendChild (localidad)
		valor = doc.createTextNode (unicode (str(direccion_partner[2]),'utf-8'))
		localidad.appendChild (valor)

		provincia = doc.createElement ("provincia")
		informacion_comprador.appendChild (provincia)
		valor = doc.createTextNode (unicode (str(direccion_partner[3]),'utf-8'))
		provincia.appendChild (valor)

		cp = doc.createElement ("cp")
		informacion_comprador.appendChild (cp)
		valor = doc.createTextNode (unicode (str(direccion_partner[4]),'utf-8'))
		cp.appendChild (valor)

	
		return ()


	def genera_detalle_factura (self,lineafact,cr, doc,lote_comprobantes, comprobante, detalle, nro_linea, temp_buffer):


		linea = doc.createElement ("linea")
		detalle.appendChild (linea)
		linea.setAttribute ("numeroLinea",str (nro_linea))


		descripcion = doc.createElement ("descripcion")
		linea.appendChild (descripcion)
		valor = doc.createTextNode (unicode (str(lineafact.name),'utf-8'))
		descripcion.appendChild (valor)

		cantidad = doc.createElement ("cantidad")
		linea.appendChild (cantidad)
		valor = doc.createTextNode (str(lineafact.quantity))
		cantidad.appendChild (valor)

		precio_unitario = doc.createElement ("precio_unitario")
		linea.appendChild (precio_unitario)
		valor = doc.createTextNode (str(abs(lineafact.price_unit)))
		precio_unitario.appendChild (valor)

		importe_total_articulo = doc.createElement ("importe_total_articulo")
		linea.appendChild (importe_total_articulo)
		valor = doc.createTextNode (str(abs(lineafact.price_subtotal)))
		importe_total_articulo.appendChild (valor)

	# El valor que aparece como código de impuesto será multiplicado la cantidad por 100

		alicuota_iva = doc.createElement ("alicuota_iva")
		linea.appendChild (alicuota_iva)
	
		tasa_impuesto = [ t.amount for t in lineafact.invoice_line_tax_id ]
	
		valor = doc.createTextNode (str(tasa_impuesto[0]*100))
		alicuota_iva.appendChild (valor)

		return ()


	def genera_resumen_factura (self,invoice,cr, doc,lote_comprobantes, comprobante, temp_buffer):
	#	GENERA EL RESUMEN DE CADA FACTURA

		resumen = doc.createElement ("resumen")
		comprobante.appendChild (resumen)

		importe_total_neto_gravado = doc.createElement ("importe_total_neto_gravado")
		resumen.appendChild (importe_total_neto_gravado)
		valor = doc.createTextNode (str("%.2f" % abs(invoice.amount_untaxed)))
		importe_total_neto_gravado.appendChild (valor)

		importe_total_concepto_no_gravado = doc.createElement ("importe_total_concepto_no_gravado")
		resumen.appendChild (importe_total_concepto_no_gravado)
		valor = doc.createTextNode ("0.00")
		importe_total_concepto_no_gravado.appendChild (valor)

		importe_operaciones_exentas = doc.createElement ("importe_operaciones_exentas")
		resumen.appendChild (importe_operaciones_exentas)
		valor = doc.createTextNode ("0.00")
		importe_operaciones_exentas.appendChild (valor)

		impuesto_liq = doc.createElement ("impuesto_liq")
		resumen.appendChild (impuesto_liq)
		valor = doc.createTextNode (str("%.2f" % abs(invoice.amount_tax)))
		impuesto_liq.appendChild (valor)

		impuesto_liq_rni = doc.createElement ("impuesto_liq_rni")
		resumen.appendChild (impuesto_liq_rni)
		valor = doc.createTextNode ("0.00")
		impuesto_liq_rni.appendChild (valor)


		importe_total_impuestos_nacionales = doc.createElement ("importe_total_impuestos_nacionales")
		resumen.appendChild (importe_total_impuestos_nacionales)
		valor = doc.createTextNode ("0.00")
		importe_total_impuestos_nacionales.appendChild (valor)

		importe_total_ingresos_brutos = doc.createElement ("importe_total_ingresos_brutos")
		resumen.appendChild (importe_total_ingresos_brutos)
		valor = doc.createTextNode ("0.00")
		importe_total_ingresos_brutos.appendChild (valor)

		importe_total_impuestos_municipales = doc.createElement ("importe_total_impuestos_municipales")
		resumen.appendChild (importe_total_impuestos_municipales)
		valor = doc.createTextNode ("0.00")
		importe_total_impuestos_municipales.appendChild (valor)

		importe_total_impuestos_internos = doc.createElement ("importe_total_impuestos_internos")
		resumen.appendChild (importe_total_impuestos_internos)
		valor = doc.createTextNode ("0.00")
		importe_total_impuestos_internos.appendChild (valor)


		importe_total_factura = doc.createElement ("importe_total_factura")
		resumen.appendChild (importe_total_factura)
		valor = doc.createTextNode (str("%.2f" % abs(invoice.amount_total)))
		importe_total_factura.appendChild (valor)

		tipo_de_cambio = doc.createElement ("tipo_de_cambio")
		resumen.appendChild (tipo_de_cambio)
		valor = doc.createTextNode (str(invoice.currency_id.rate))
		tipo_de_cambio.appendChild (valor)

		codigo_moneda = doc.createElement ("codigo_moneda")
		resumen.appendChild (codigo_moneda)
		valor = doc.createTextNode (str(invoice.currency_id.afip))
		codigo_moneda.appendChild (valor)

		observaciones = doc.createElement ("observaciones")
		resumen.appendChild (observaciones)
		if invoice.comment == 0:
			temp_val = '' 
		else :
			temp_val = invoice.comment
		valor = doc.createTextNode (str(temp_val))
		observaciones.appendChild (valor)


		return ()





	_name="invoice.wizard.genera.cae"
	_columns = {
		'archivo_destino': fields.binary('Archivo', filters="*.xml"),
		'nombre': fields.char('Nombre de Archivo', size=32),
 		}
	_defaults = {
		'nombre' : lambda *a: 'cae.xml'
		}


genera_formulario_cae ()
