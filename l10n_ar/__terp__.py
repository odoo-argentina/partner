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

{
    'name': 'Localization for Argentina',
    'version': '1.0',
    'author': 'Thymbra - Torre de Hanoi',
    'category': 'Localisation/Argentina',
    'website': 'http://www.thymbra.com/',
    'license': 'GPL-3',
    'description': """
Localization Model of Argentina
Includes:
 - Provinces
 - Denominations of Partners and Contacts
 - Added check the validity of that VAT Number for Argentina

""",
    'depends': [
        'base',
        'account',
    ],
    'init_xml': [],
    'demo_xml': [],
    'update_xml': [
        'res_country_states.xml',
        'res_partner_title.xml',
    ],
    'active': False,
    'installable': True,
}
