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


class ItemuseApplicationLine(models.Model):
    _name = 'oa.itemuse.application.line'
    _description = "物品领用明细"

    oa_itemuse_id = fields.Many2one(comodel_name='oa.itemuse.application', string=u'物品领用', ondelete='cascade')
    sequence = fields.Integer(string=u'序号')
    itemuse = fields.Char(string='物品名称', required=True)
    item_number = fields.Char(string='数量', required=True)
    remarks = fields.Char(string='备注')


class ItemuseApplication(models.Model):
    _name = 'oa.itemuse.application'
    _inherit = ['oa.base.model']
    _description = "物品领用"
    _rec_name = 'emp_id'

    emp_id = fields.Many2one(comodel_name='hr.employee', string=u'领用人', required=True)
    reason_leave = fields.Text(string=u'物品用途', required=True)
    remarks = fields.Text(string=u'领用详情')
    line_ids = fields.One2many(comodel_name='oa.itemuse.application.line', inverse_name='oa_itemuse_id', string=u'物品明细')

    @api.model
    def create(self, values):
        values['form_number'] = self.env['ir.sequence'].sudo().next_by_code('oa.itemuse.application.code')
        return super(ItemuseApplication, self).create(values)
