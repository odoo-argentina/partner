#!/usr/bin/env python
# (C) 2006 Thymbra
# License: GPL
# Small script to create an Chart of Account xml encoded file from csv

import sys
import csv

print '<?xml version="1.0" encoding="utf-8"?>'
print '<openerp>'
print '    <data noupdate="True">'
print ''

csv_file = csv.reader(open(sys.argv[1], 'rb'))

for line in csv_file:
    print '    <record model="account.account.template" id="' + line[1] + '">'
    print '        <field name="name">%s</field>' % line[3]
    print '        <field name="code">%s</field>' % line[0]
    print '        <field name="type">%s</field>' % line[2]
    print '        <field name="user_type" ref="account_type_%s"/>' % line[2]
    print '        <field ref="%s" name="parent_id"/>' % line[4]
    print '    </record>'

print ''
print '    </data>'
print '</openerp>'
print ''
