# -*- coding: utf-8 -*-
###################################################################################
#    Copyright (C) 2019 SuXueFeng License（apache）
###################################################################################
{
    'name': "流程申请-财务管理",
    'summary': """流程申请-财务管理""",
    'description': """流程申请-财务管理""",
    'author': "SuXueFeng",
    'website': "https://www.sxfblog.com",
    'category': 'oa',
    'version': '1.0',
    'depends': ['odoo_oa_base'],
    'installable': True,
    'application': False,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'data/default_num.xml',
    ]
}
