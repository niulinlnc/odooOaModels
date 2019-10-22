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


class TransferAppliction(models.Model):
    _name = 'oa.transfer.appliction'
    _inherit = ['oa.base.model']
    _description = "调岗申请"
    _rec_name = 'emp_id'

    emp_id = fields.Many2one(comodel_name='hr.employee', string=u'申请人', required=True)
    dept_id = fields.Many2one(comodel_name='hr.department', string=u'原部门', required=True)
    job_id = fields.Many2one(comodel_name='hr.job', string=u'原职位', required=True)
    new_dept_id = fields.Many2one(comodel_name='hr.department', string=u'转入部门', required=True)
    new_job_id = fields.Many2one(comodel_name='hr.job', string=u'转入职位', required=True)
    effective_date = fields.Date(string=u'生效日期')
    reason = fields.Text(string=u'调岗原因', required=True)

    @api.onchange('emp_id')
    def onchange_emp_id(self):
        if self.emp_id:
            self.dept_id = self.emp_id.department_id.id
            self.job_id = self.emp_id.job_id.id

    @api.model
    def create(self, values):
        values['form_number'] = self.env['ir.sequence'].sudo().next_by_code('oa.transfer.application.code')
        return super(TransferAppliction, self).create(values)


