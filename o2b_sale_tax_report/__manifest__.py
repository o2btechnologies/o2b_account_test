# -*- coding: utf-8 -*-
##########################################################################
# Author      : O2b Technologies Pvt. Ltd.(<www.o2btechnologies.com>)
# Copyright(c): 2016-Present O2b Technologies Pvt. Ltd.
# All Rights Reserved.
#
# This program is copyright property of the author mentioned above.
# You can`t redistribute it and/or modify it.
#
##########################################################################
{
    "name": "O2B Sale Tax Report",
    'summary': 'O2b Sale Tax Report',
    "version": "11.0.0.1",
    "author": "O2b Technologies",
    'website': 'https://www.o2btechnologies.com',
    "depends": ['base', 'sale','web','account','product'],
    "description": """
                O2b Sale tax Report
      """,
    "data": [
                'security/ir.model.access.csv',
                'views/commission_report.xml',
                
                
                
            ],
    "installable": True,
}

# vim:expandtab:smartindent:tabstop=4:softtabstop=4:shiftwidth=4:
