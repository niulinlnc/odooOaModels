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
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class ReissueApplication(models.Model):
    _name = 'oa.reissue.application'
    _inherit = ['oa.base.model']
    _description = "补签申请"

    emp_id = fields.Many2one(comodel_name='hr.employee', string=u'补签人', required=True)
    reissue_date = fields.Date(string=u'补签日期', required=True)
    reissue_type = fields.Selection(string=u'补签类型', selection=[('上班卡', '上班卡'), ('下班卡', '下班卡'), ],
                                    default='上班卡', required=True)
    reissue_text = fields.Char(string=u'补签事由', required=True)

    @api.model
    def create(self, values):
        values['form_number'] = self.env['ir.sequence'].sudo().next_by_code('oa.reissue.application.code')
        return super(ReissueApplication, self).create(values)
