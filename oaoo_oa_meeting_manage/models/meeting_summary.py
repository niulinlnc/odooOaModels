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

import logging
from odoo import models, fields, api, exceptions
from odoo import SUPERUSER_ID
from odoo.exceptions import UserError
import uuid

logger = logging.getLogger(__name__)


class MeetingSummary(models.Model):
    _name = 'oa.meeting.meeting.summary'
    _inherit = ['mail.thread', 'ir.needaction_mixin']
    _rec_name = 'meeting_title'
    _description = u'会议纪要'

    meeting_title = fields.Many2one('oa.meeting.meeting.application', string=u'所属会议', required=True)
    # model_name = fields.Char(u'模型', store=1, index=1)
    # res_id = fields.Integer(u'记录ID', store=1)
    user_id = fields.Many2one('res.users', string=u'记录人', readonly=True, default=lambda self: self.env.user)
    company_id = fields.Many2one('res.company', string=u'所属公司', default=lambda self: self.env.user.company_id)
    release_time = fields.Datetime(string=u'发布时间', placeholder=u"当前系统时间")
    meeting_summary = fields.Html(string=u'纪要内容')
    summary_file = fields.Many2many('ir.attachment', string=u'上传附件')
    meeting_members = fields.Many2many('res.users', string=u'抄送至')
    check_state = fields.Boolean(default=False)
    active = fields.Boolean('Active', default=True)
    state = fields.Selection([('init', u'暂存'), ('release', u'已发布')], string=u'发布状态', readonly=True)
    uuid = fields.Char('UUID', default=lambda s: uuid.uuid4(), copy=False, required=True)
    super_id = fields.Integer(default=SUPERUSER_ID)

    _sql_constraints = [
        ('uuid_uniq', 'unique (uuid)', u"UUID存在重复列，请重试"),
    ]

    @api.multi
    def unlink(self):
        for line in self:
            if line.state == 'release':
                raise UserError(u'您不能删除已经发布的纪要文件')
            else:
                sql = """
                    UPDATE oa_meeting_meeting_application SET copy_state = 'unpublished' WHERE id = %s
                """ % line.meeting_title.id
                line.env.cr.execute(sql)
        return super(MeetingSummary, self).unlink()

    @api.multi
    def change_state(self):
        self.write({'state': 'release'})
        self.write({'check_state': True})
        self.send_summary()

    @api.onchange('meeting_title')
    def _onchange_meeting_title(self):
        for line in self:
            if line.meeting_title:
                line.meeting_members = line.meeting_title.employee_ids

    def send_summary(self):
        mail_meeting_message = self.env.ref('oa_meeting.mail_meeting_message')
        model_name = self.env['ir.model'].search([('model', '=', self._name)]).name
        self.env['mail.message'].sudo().create({
            'subject': self._name,
            'model': self._name,
            'res_id': self.id,
            'record_name': model_name,
            'body': u'<p>给您抄送了一份会议纪要</p>',
            'partner_ids': [(6, 0, [user.partner_id.id for user in self.meeting_members])],
            'channel_ids': [(6, 0, [mail_meeting_message.id])],
            'message_type': 'notification',
            'author_id': self.env.user.partner_id.id
        })

    @api.model
    def create(self, vals):
        vals['state'] = 'init'
        result = super(MeetingSummary, self).create(vals)
        return result

    @api.constrains('meeting_title')
    def constraint_member_ids(self):
        for line in self:  # 改变该次会议的标识，使其不可再创建会议纪要
            if not line.meeting_title.approval_state:
                line.meeting_title.copy_state = 'published'
            else:
                sql = """
                    UPDATE oa_meeting_meeting_application SET copy_state = 'published' WHERE id = %s
                """ % line.meeting_title.id
                line.env.cr.execute(sql)
