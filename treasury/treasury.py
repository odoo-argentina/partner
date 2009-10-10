# coding=utf-8

#    Copyright (C) 2008  Luis Falcon

#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.




from osv import fields, osv

class treasury_document (osv.osv):
	_name = "account.treasury"
	_columns = {
                'partner_id' : fields.many2one('res.partner','Partner', required='1', help="Partner"), 
                'document_id' : fields.char('Document ID',size=64, required='1', help="Partner"), 
		'reference' : fields.char('Reference', select=True,size=64,help="Partner"),
		'info' : fields.text('Comments'),
		'amount': fields.float('Amount', digits=(16,2),select=True),
		'document_emission_date' : fields.date('Emission Date',select=True),
		'document_clearing_date' : fields.date ('Clearing Date',select=True),
		'bank_source' : fields.many2one ('res.bank','Source Bank',select=True,help="Source Bank"),
		'bank_target' : fields.many2one ('res.bank','Target Bank',select=True,help="Target Bank"),
		'third_party' : fields.boolean ('To/From 3rd party',help="Document coming from or endorsed to a third party partner"),
		'third_party_partner' : fields.many2one('res.partner','3rd Party Partner', help="Partner"),
		'document_type' : fields.selection([
                                ('ch','check'),
                                ('tr','transfer'),
				('ca','cash'),
				('co','coupon'),
				('cc','credit card'),
                                ], 'Document Type'),

		'document_op' : fields.selection([
                                ('p','Payable'),
                                ('r','Receivable'),
                                ], 'Operation'),

		'document_status' : fields.selection([
                                ('o','Open'),
                                ('p','Being processed'),
                                ('c','Cleared'),
                                ('x','Cancelled'),
                                 ], 'Document Status'),
		}

treasury_document ()

