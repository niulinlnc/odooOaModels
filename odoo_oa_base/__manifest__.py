# -*- coding: utf-8 -*-
###################################################################################
# Copyright (C) 2019 SuXueFeng
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###################################################################################
{
    'name': "流程申请",
    'summary': """用于odoo流程申请的表单和单据""",
    'description': """用于odoo流程申请的表单和单据""",
    'author': "SuXueFeng",
    'website': "http://sxfblog.com",
    'category': 'oa',
    'version': '1.0',
    'installable': True,
    'application': True,
    'auto_install': False,
    'depends': ['hr', 'contacts', 'document'],
    'data': [
        'data/base_ir_rule.xml',
        'groups/group.xml',
        'views/assets.xml',
    ]
}
