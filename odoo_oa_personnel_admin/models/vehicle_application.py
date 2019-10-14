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


class VehicleApplicationLine(models.Model):
    _name = 'oa.vehicle.application.line'
    _description = "用车申请列表"

    oa_vehicle_id = fields.Many2one(comodel_name='oa.vehicle.application', string=u'用车申请', ondelete='cascade')
    sequence = fields.Integer(string=u'序号')
    fleet_id = fields.Many2one(comodel_name='fleet.vehicle', string=u'车辆', required=True)
    license_plate = fields.Char(string='车牌号', required=True)
    emp_id = fields.Many2one(comodel_name='res.partner', string=u'驾驶员', required=True)
    remarks = fields.Char(string='备注')

    @api.onchange('fleet_id')
    def onchange_fleet_id(self):
        if self.fleet_id:
            self.license_plate = self.fleet_id.license_plate
            self.emp_id = self.fleet_id.driver_id.id


class VehicleApplication(models.Model):
    _name = 'oa.vehicle.application'
    _inherit = ['oa.base.model']
    _description = "用车申请"
    _rec_name = 'emp_id'

    emp_id = fields.Many2one(comodel_name='hr.employee', string=u'申请人', required=True)
    dept_id = fields.Many2one(comodel_name='hr.department', string=u'申请部门', required=True)
    reason_leave = fields.Text(string=u'用车事由', required=True)
    start_add = fields.Char(string='始发地点', required=True)
    end_add = fields.Char(string='返回地点', required=True)
    use_date = fields.Date(string=u'用车日期', required=True)
    end_date = fields.Date(string=u'返回日期')
    line_ids = fields.One2many(comodel_name='oa.vehicle.application.line', inverse_name='oa_vehicle_id', string=u'用车列表')

    @api.onchange('emp_id')
    def onchange_emp_id(self):
        if self.emp_id:
            self.dept_id = self.emp_id.department_id.id

    @api.model
    def create(self, values):
        values['form_number'] = self.env['ir.sequence'].sudo().next_by_code('oa.vehicle.application.code')
        return super(VehicleApplication, self).create(values)
