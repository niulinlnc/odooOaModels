# -*- coding: utf-8 -*-
###################################################################################
#    Copyright (C) 2019 SuXueFeng
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU Affero General Public License as
#    published by the Free Software Foundation, either version 3 of the
#    License, or (at your option) any later version.
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU Affero General Public License for more details.
#    You should have received a copy of the GNU Affero General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>.
###################################################################################
import logging
from odoo import api, fields, models

_logger = logging.getLogger(__name__)


class OaBaseModel(models.Model):
    _name = 'oa.base.model'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = "流程审批表单基类"
    _rec_name = 'form_number'

    active = fields.Boolean(string=u'Active', default=True)
    name = fields.Char(string='标题', required=True)
    form_number = fields.Char(string='单据编号', index=True, copy=False)
    company_id = fields.Many2one('res.company', string='公司', default=lambda self: self.env.user.company_id.id)
    remarks = fields.Text(string=u'备注')
    attachment_number = fields.Integer(compute='_compute_attachment_number', string='附件')

    def attachment_image_preview(self):
        self.ensure_one()
        domain = [('res_model', '=', self._name), ('res_id', '=', self.id)]
        return {
            'domain': domain,
            'res_model': 'ir.attachment',
            'name': u'附件管理',
            'type': 'ir.actions.act_window',
            'view_id': False,
            'view_mode': 'kanban,tree,form',
            'view_type': 'form',
            'limit': 20,
            'context': "{'default_res_model': '%s','default_res_id': %d}" % (self._name, self.id)
        }

    def _compute_attachment_number(self):
        attachment_data = self.env['ir.attachment'].read_group(
            [('res_model', '=', self._name), ('res_id', 'in', self.ids)], ['res_id'], ['res_id'])
        attachment = dict((data['res_id'], data['res_id_count']) for data in attachment_data)
        for expense in self:
            expense.attachment_number = attachment.get(expense.id, 0)