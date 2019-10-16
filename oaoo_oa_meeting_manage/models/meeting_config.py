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

from odoo import models, fields, api, _
import datetime
import logging

logger = logging.getLogger(__name__)


class BoardroomManagement(models.Model):
    _inherit = ['mail.thread']
    _name = 'oa.meeting.room.manage'
    _rec_name = 'name'
    _description = u"会议室管理"

    name = fields.Char(string=u'会议室名称', required=True)
    create_uid = fields.Many2one('res.users', string=u'填写人姓名', default=lambda self: self.env.user)
    department_id = fields.Many2one('hr.department', string=u'填写人部门')
    company_id = fields.Many2one('res.company', string=u'填写人公司', default=lambda self: self.env.user.company_id.id)
    active = fields.Boolean(string=u'是否启用', default=True)
    state = fields.Selection([('using', u'使用中'), ('idle', u'闲置')], string=u'使用情况', default='idle')
    address = fields.Char(string=u'会议室地址')
    size = fields.Integer(string=u'座位数')
    boardroom_configure = fields.Many2many('oa.meeting.room.configure', string=u'会议室配置')
    boardroom_manager = fields.Many2one('res.users', string=u'会议室管理员')
    create_date = fields.Date(string=u'启用时间', default=datetime.date.today())
    remarks = fields.Text(string=u'备注')

    _sql_constraints = [
        ('name', 'unique (name)', u"U请不要重复创建会议室!"),
    ]


class BoardroomConfigure(models.Model):
    _name = 'oa.meeting.room.configure'
    _rec_name = 'name'
    _description = u'会议室配置信息'

    state = fields.Boolean(string='是否启用', default=True)
    name = fields.Char(string=u'设备名称')
    company_id = fields.Many2one('res.company', string=u'所属公司',
                                 default=lambda self: self.env.user.company_id)
    configure_info = fields.Text(string=u'设备说明')


class BoardRoomType(models.Model):
    _name = 'oa.meeting.type'
    _rec_name = 'name'
    _description = u'会议类型'

    state = fields.Boolean(string='是否启用', default=True)
    name = fields.Char(string=u'类型名称')
    configure_info = fields.Text(string=u'说明')
