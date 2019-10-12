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
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class OvertimeApplication(models.Model):
    _name = 'oa.overtime.application'
    _inherit = ['oa.base.model']
    _description = "加班申请"

    emp_id = fields.Many2one(comodel_name='hr.employee', string=u'申请人', required=True)
    start_date = fields.Datetime(string=u'开始时间', required=True)
    end_date = fields.Datetime(string=u'结束时间', required=True)
    duration = fields.Integer(string=u'时长(小时)')
    reason_leave = fields.Text(string=u'加班原因', required=True)

    @api.model
    def create(self, values):
        values['form_number'] = self.env['ir.sequence'].sudo().next_by_code('oa.overtime.application.code')
        return super(OvertimeApplication, self).create(values)