# -*- coding: utf-8 -*-
###################################################################################
# Copyright (C) 2019 SuXueFeng
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#     http://www.apache.org/licenses/LICENSE-2.0
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
###################################################################################
{
    'name': "流程申请-会议管理",
    'summary': """流程申请-会议管理""",
    'description': """ 流程申请-会议管理模块""",
    'author': "SuXueFeng",
    'category': 'oa',
    'version': '1.0',
    'depends': ['odoo_oa_base'],
    'installable': False,
    'auto_install': False,
    'data': [
        'security/ir.model.access.csv',
        'groups/group.xml',
        # 会议配置
        'views/meeting_config.xml',
        # 会议申请
        'views/meeting_application.xml',
        # 会议纪要
        # 'views/meeting_meeting_summary.xml',
    ],
}
