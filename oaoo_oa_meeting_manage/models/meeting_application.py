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

from odoo import fields, models
import logging

_logger = logging.getLogger(__name__)


class MeetingApplication(models.Model):
    _name = 'oa.meeting.meeting.application'
    _inherit = ['mail.thread']
    _rec_name = 'meeting_name'
    _description = u"会议申请"

    meeting_name = fields.Char(string=u'主题', required=True)
    start_time = fields.Datetime(string=u'开会时间', required=True)
    end_time = fields.Datetime(string=u'结束时间', required=True)
    create_uid = fields.Many2one('res.users', string=u'会议发起人', default=lambda self: self.env.user)
    user_info_id = fields.Many2one('hr.employee', string=u"会议申请人")
    department_id = fields.Many2one('hr.department', string=u'发起人部门')
    host_id = fields.Many2one('res.users', string=u'会议主持人', required=True)
    company_id = fields.Many2one('res.company', default=lambda self: self.env.user.company_id.id, readonly=True,
                                 string=u'公司')
    meeting_address = fields.Many2one('oa.meeting.room.manage', string=u'会议室', required=True)
    meeting_recorder = fields.Many2one('res.users', string=u'会议记录人', required=True)
    meeting_type = fields.Many2one('oa.meeting.type', string=u'会议类型', required=True)
    meeting_remind = fields.Selection([
        ('nothing', u'无'),
        ('twenty', u'20分钟'),
        ('thirty', u'30分钟'),
        ('an_hour', u'1小时'),
        ('two_hours', u'2小时'),
        ('twelve_hours', u'12小时'),
        ('one_day', u'1天'),
        ('two_days', u'2天'),
        ('week', u'1周')], string=u'会议提醒')
    employee_ids = fields.Many2many(comodel_name='res.users', relation='meeting_and_res_users_rel',
                                    column1='meeting_id', column2='user_id', string=u'参与人员', required=True)
    meeting_enclosure = fields.Many2many('ir.attachment', string=u'议题文件')
    meeting_info = fields.Text(string=u'会议简要')
    meeting_need = fields.Many2many('oa.meeting.room.configure', string=u'会议设备')
    create_date = fields.Datetime(string=u'发布时间')
    state = fields.Selection(string=u'会议状态', selection=[('00', u'未开始'), ('01', u'会议中'), ('02', u'已结束'), ('03', u'已取消')],
                             default='00')

# @api.multi
# def unlink(self):
# 	for line in self:
# 		if line.meeting_state != 'not_begin' and line.meeting_state != 'cancel':
# 			raise ValidationError(u'此会议已经开始或结束，您不能删除该记录')
# 		return super(MeetingApplication, line).unlink()
#
# @api.depends('user_id')
# def compute_check_summary(self):
# 	if self.employee_ids:
# 		if self.env.user in self.employee_ids:  # 判断查看单据的当前用户是否为参会人员
# 			self.get_summary = True
#
# @api.depends('user_id')
# def compute_check_user(self):
# 	self.ensure_one()
# 	if self.user_id:
# 		if self.env.user == self.user_id:  # 判断查看单据的当前用户是否为发起人
# 			self.get_user = True
#
# @api.depends('user_id')
# def compute_check_participant(self):
# 	if self.participant_ids and self.employee_ids:
# 		if self.env.user in self.employee_ids:
# 			temp_list = self.env['oa.meeting.partake.situation'].search([('participant_id', '=', self.env.user.id), ('meeting_info', '=', self.id)])
# 			if temp_list.attend_state == 'unconfirmed':  # 判断查看单据的当前用户是否为参会人员且未确认是否参会
# 				self.get_participant = True
#
# def cancel_meeting(self):
# 	if self.env.user == self.user_id:
# 		self.update({'meeting_state': 'cancel'})
# 	else:
# 		raise exceptions.ValidationError(u'只有会议的发起人才能取消会议')
#
# @api.multi
# def set_state(self):
# 	_logger.debug(">>>>>>>>>>>执行动作")
#
# @api.multi
# def set_meeting_state(self):
# 	"""
# 		会议模块定时任务
# 		根据当前时间设置会议状态
# 		not_begin	:	未开始
# 		started 	:	会议中
# 		finished	:	已结束
# 		cancel		:	已取消
# 		1.当前时间<会议开始时间  未开始
# 		2.当前时间>=会议开始时间 当前时间<= 会议结束时间  会议中
# 		3.会议结束
# 	"""
# 	# 搜索未开始和会议中记录
# 	record_list = self.search([('meeting_state', 'in', ['not_begin', 'started'])])
# 	now_time = datetime.datetime.now()
# 	_logger.debug(u'未开始和会议中查询记录数(%s)' % (len(record_list.ids)))
# 	i = 0
# 	for record in record_list:
# 		i += 1
# 		_logger.debug(u"循环:%s, 循环次数%s"% (record,i))
# 		# 表名
# 		table_name = record._table
# 		# 会议状态
# 		state = ''
# 		# 会议开始时间
# 		temp_begin = datetime.datetime.strptime(record.start_time, "%Y-%m-%d %H:%M:%S")
# 		# 会议结束时间
# 		temp_end = datetime.datetime.strptime(record.end_time, "%Y-%m-%d %H:%M:%S")
# 		if record.cloud_device:
# 			# 判断审批状态
# 			if record.approval_state == 'complete':
# 				# 审批完成时间
# 				success_date = datetime.datetime.strptime(record.success_date, "%Y-%m-%d %H:%M:%S")
# 				if success_date >= temp_begin:
# 					temp_begin = success_date
# 		if now_time < temp_begin:
# 			# 未开始
# 			state = 'not_begin'
# 		elif now_time >= temp_begin and now_time <= temp_end:
# 			# 会议中
# 			state = 'started'
# 		else:
# 			# 已结束
# 			state = 'finished'
# 		sql = """
# 				UPDATE %s SET meeting_state = '%s' WHERE id = %s
# 			""" % (table_name,state, record.id)
# 		_logger.debug(u'会议开始时间(%s)>>>>会议结束时间(%s)>>>>当前时间(%s)>>>>最后一次更新时间(%s)>>>会议状态(%s)'% (temp_begin, temp_end, now_time,record.write_date,state))
# 		_logger.debug(u'输出SQL(%s)' % (sql))
# 		self.env.cr.execute(sql)
#
# @api.depends('employee_ids')
# def compute_participant_state(self):
# 	"""
# 		将参会人员添加到会议确认列表中
# 	"""
# 	if self.employee_ids:
# 		temp_list = self.env['oa.meeting.partake.situation']
# 		for i in self.employee_ids:
# 			data = {
# 				'participant_id': i.id,
# 				'attend_state': 'unconfirmed',
# 				'company_id': i.company_id.id,
# 			}
# 			temp_list += temp_list.new(data)
# 		self.participant_ids = temp_list
#
# @api.onchange('user_id')
# def _onchange_user_id(self):
# 	self.employee_ids = [(6, 0, [self.user_id.id])]
#
# def attend_meeting(self):
# 	get_id = self.env.user.id
# 	for line in self.participant_ids:
# 		if line.participant_id.id == get_id:  # 将当前用户的参与状态置为参加
# 			line.update({'attend_state': 'attend'})
#
# def absence_meeting(self):
# 	get_id = self.env.user.id
# 	for line in self.participant_ids:
# 		if line.participant_id.id == get_id:  # 将当前用户的参与状态置为缺席
# 			line.update({'attend_state': 'absence'})
#
# @api.onchange('meeting_recorder', 'host_id')
# def _onchange_meeting_recorder(self):
# 	if self.host_id and self.meeting_recorder:
# 		self.employee_ids = [(6, 0, [self.meeting_recorder.id, self.host_id.id, self.user_id.id])]
# 	elif self.meeting_recorder:
# 		self.employee_ids = [(6, 0, [self.meeting_recorder.id, self.user_id.id])]
# 	elif self.host_id:
# 		self.employee_ids = [(6, 0, [self.host_id.id, self.user_id.id])]
#
# @api.onchange('member_group')
# def _onchange_members_group(self):
# 	if self.member_group:
# 		self.employee_ids += self.member_group.group_ids
#
# @api.onchange('meeting_address')
# def _onchange_meeting_need(self):
# 	if self.meeting_address:
# 		self.meeting_need = self.meeting_address.boardroom_configure
#
# @api.constrains('start_time', 'end_time', 'meeting_address')
# def _constraint_time(self):
# 	if datetime.datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S") < datetime.datetime.now():
# 		raise exceptions.ValidationError(u"会议开始时间不能小于当前时间")
#
# 	elif self.end_time <= self.start_time:
# 		raise exceptions.ValidationError(u"会议结束时间必须大于开始时间")
#
# 	temp_model = self.search([['meeting_address.boardroom_name', '=', self.meeting_address.boardroom_name]])
# 	for line in temp_model:
# 		if line.id != self.id:
# 			if line.end_time >= self.start_time and line.start_time <= self.end_time:
# 				raise exceptions.ValidationError(u"该会议室在您所选时间段内被使用，请重新选择")
#
# @api.constrains('meeting_need')
# def _constraint_meeting_need(self):
# 	if self.meeting_need:
# 		temp_model = self.search([('meeting_need.id', 'in', self.meeting_need.ids)])
# 		for line in temp_model:
# 			if line.id != self.id:
# 				if line.end_time >= self.start_time and line.start_time <= self.end_time:
# 					raise exceptions.ValidationError(u"需求资源中含有在您所选时间段内被使用的设备，请重新选择")
#
# @api.depends('user_id')
# def _compute_department_id(self):
# 	for line in self:
# 		line.department_id = line.user_id.employee_ids[:1].department_id
#
# def send_summary(self):
# 	"""
# 		给参会人员发送消息
# 	"""
# 	temp_begin = datetime.datetime.strptime(self.start_time, "%Y-%m-%d %H:%M:%S")
# 	table_name = self._name.replace('.', '_')
# 	if temp_begin <= datetime.datetime.now():
# 		sql = """
# 			UPDATE %s SET meeting_state = 'started' WHERE id = %s
# 		""" % (table_name, self.id)
# 		self.env.cr.execute(sql)
#
# 	if self.approval_state:
# 		sql = """
# 			UPDATE %s SET approval_state = 'complete' WHERE id = %s
# 		""" % (table_name, self.id)
# 		self.env.cr.execute(sql)
#
# 	mail_meeting_message = self.env.ref('oa_meeting.mail_meeting_message')
# 	model_name = self.env['ir.model'].search([('model', '=', self._name)]).name
# 	self.env['mail.message'].sudo().create({
# 		'subject': self._name,
# 		'model': self._name,
# 		'res_id': self.id,
# 		'record_name': model_name,
# 		'body': u'<p>发起了一个新会议邀请您参加</p>',
# 		'partner_ids': [(6, 0, [user.partner_id.id for user in self.employee_ids])],
# 		'channel_ids': [(6, 0, [mail_meeting_message.id])],
# 		'message_type': 'notification',
# 		'author_id': self.env.user.partner_id.id
# 	})
#
# @api.model
# def create(self, vals):
# 	vals['meeting_state'] = 'not_begin'
# 	result = super(MeetingApplication, self).create(vals)
# 	return result
#
# @api.constrains('user_id')
# def check_approval_stat(self):
# 	temp_list = self.env['ir.model'].search([('model', '=', self._name)]).id
# 	temp_model = self.env['approval.flow'].search([('model_id', '=', temp_list)])
# 	temp_check = False
# 	if temp_model.condition:
# 		temp_check = self.env['oa.meeting.meeting.application'].search(eval(temp_model.condition))
#
# 	if temp_model.company_ids:  # 判断是否走审批流
# 		if self.env.user.company_id in temp_model.company_ids:
# 			if temp_check:
# 				if self.id in temp_check.ids:
# 					self.approval_state = 'init'
# 				else:
# 					self.send_summary()
# 			else:
# 				self.approval_state = 'init'
# 		else:
# 			self.send_summary()
#
# 	elif temp_check:
# 		if self.id in temp_check.ids:
# 			self.approval_state = 'init'
# 		else:
# 			self.send_summary()
#
# 	else:
# 		self.send_summary()

# class PartakeSituation(models.Model):
# 	_name = 'oa.meeting.partake.situation'
# 	_rec_name = 'participant_id'
# 	_description = u'会议人员参与情况'
#
# 	participant_id = fields.Many2one('res.users', string=u'参与人员')
# 	attend_state = fields.Selection([('attend', u'参加'), ('absence', u'缺席'), ('unconfirmed', u'未确认')], string=u'参与状态', default='unconfirmed')
# 	company_id = fields.Many2one('res.company', string=u'所属公司')
# 	meeting_info = fields.Many2one('oa.meeting.meeting.application', string=u'参与会议主题')
