#!/usr/bin/python
# (C) 2006 Thymbra
# License : GPL
# Small script to create an Chart of Account xml encoded file from csv 

import sys
import csv

print "<?xml version=\"1.0\" encoding=\"utf-8\" ?>\n<openerp>\n<data noupdate=\"True\">"

csv_file = csv.reader(open(sys.argv[1], 'rb'))

for line in csv_file:
	print "<record model=\"account.account.template\" id=\""+line[1]+"\">"
	print "\t<field name=\"name\">"+line[3]+"</field>"
	print "\t<field name=\"code\">"+line[0]+"</field>"
	print "\t<field name=\"type\">"+line[2]+"</field>"
	print "\t<field name=\"user_type\" ref=\"account_type_"+line[2]+"\"/>"
	print "\t<field ref=\""+line[4]+"\" name=\"parent_id\"/>"
	print "</record>"

print "</data>\n</openerp>"

