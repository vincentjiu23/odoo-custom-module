# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class CustomRecord(models.Model):
    _name = 'custom.record'
    _description = 'Custom Record'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _order = 'priority desc, date desc, id desc'

    name = fields.Char(
        string='Reference',
        required=True,
        copy=False,
        readonly=True,
        index=True,
        default=lambda self: _('New'),
    )
    title = fields.Char(
        string='Title',
        required=True,
        tracking=True,
    )
    partner_id = fields.Many2one(
        comodel_name='res.partner',
        string='Customer / Partner',
        tracking=True,
        index=True,
    )
    user_id = fields.Many2one(
        comodel_name='res.users',
        string='Assigned To',
        default=lambda self: self.env.user,
        tracking=True,
        index=True,
    )
    company_id = fields.Many2one(
        comodel_name='res.company',
        string='Company',
        default=lambda self: self.env.company,
        required=True,
    )
    currency_id = fields.Many2one(
        comodel_name='res.currency',
        string='Currency',
        related='company_id.currency_id',
        readonly=True,
    )
    amount = fields.Monetary(
        string='Estimated Amount',
        currency_field='currency_id',
        tracking=True,
        default=0.0,
    )
    date = fields.Date(
        string='Document Date',
        default=fields.Date.context_today,
        required=True,
        tracking=True,
    )
    deadline = fields.Date(
        string='Deadline',
        tracking=True,
    )
    is_overdue = fields.Boolean(
        string='Is Overdue',
        compute='_compute_is_overdue',
        store=True,
    )
    state = fields.Selection(
        selection=[
            ('draft', 'Draft'),
            ('in_progress', 'In Progress'),
            ('approved', 'Approved'),
            ('done', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='Status',
        default='draft',
        required=True,
        tracking=True,
        index=True,
    )
    priority = fields.Selection(
        selection=[
            ('0', 'Normal'),
            ('1', 'Low'),
            ('2', 'High'),
            ('3', 'Very High'),
        ],
        string='Priority',
        default='0',
    )
    tag_ids = fields.Many2many(
        comodel_name='custom.tag',
        string='Tags',
    )
    description = fields.Html(
        string='Description',
    )
    notes = fields.Text(
        string='Internal Notes',
    )
    active = fields.Boolean(
        string='Active',
        default=True,
    )

    @api.depends('deadline', 'state')
    def _compute_is_overdue(self):
        today = fields.Date.context_today(self)
        for record in self:
            if record.deadline and record.state not in ('done', 'cancelled'):
                record.is_overdue = record.deadline < today
            else:
                record.is_overdue = False

    @api.constrains('amount')
    def _check_amount(self):
        for record in self:
            if record.amount < 0:
                raise ValidationError(_("Estimated Amount cannot be negative."))

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if vals.get('name', _('New')) == _('New'):
                vals['name'] = self.env['ir.sequence'].next_by_code('custom.record.seq') or _('New')
        return super(CustomRecord, self).create(vals_list)

    def action_in_progress(self):
        self.write({'state': 'in_progress'})
        self.message_post(body=_("Status changed to <b>In Progress</b>."))

    def action_approve(self):
        self.write({'state': 'approved'})
        self.message_post(body=_("Record has been <b>Approved</b>."))

    def action_done(self):
        self.write({'state': 'done'})
        self.message_post(body=_("Record marked as <b>Completed</b>."))

    def action_cancel(self):
        self.write({'state': 'cancelled'})
        self.message_post(body=_("Record has been <b>Cancelled</b>."))

    def action_draft(self):
        self.write({'state': 'draft'})
        self.message_post(body=_("Record reset to <b>Draft</b>."))
