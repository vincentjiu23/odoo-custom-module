# -*- coding: utf-8 -*-
from odoo import models, fields, api, _
from odoo.exceptions import UserError


class CustomRecordWizard(models.TransientModel):
    _name = 'custom.record.wizard'
    _description = 'Batch Status Update Wizard'

    record_ids = fields.Many2many(
        comodel_name='custom.record',
        string='Selected Records',
        default=lambda self: self._default_record_ids(),
    )
    target_state = fields.Selection(
        selection=[
            ('in_progress', 'In Progress'),
            ('approved', 'Approved'),
            ('done', 'Completed'),
            ('cancelled', 'Cancelled'),
        ],
        string='New Status',
        required=True,
        default='approved',
    )
    reason = fields.Text(
        string='Reason / Remarks',
        required=True,
    )

    @api.model
    def _default_record_ids(self):
        active_ids = self._context.get('active_ids', [])
        return [(6, 0, active_ids)]

    def action_apply(self):
        self.ensure_one()
        if not self.record_ids:
            raise UserError(_("No records selected for status update."))

        state_labels = dict(self._fields['target_state'].selection)
        new_state_label = state_labels.get(self.target_state, self.target_state)

        for record in self.record_ids:
            record.write({'state': self.target_state})
            record.message_post(
                body=_("Batch Status Update by <b>%s</b> to <b>%s</b>.<br/>Reason: %s") % (
                    self.env.user.name,
                    new_state_label,
                    self.reason
                )
            )

        return {'type': 'ir.actions.act_window_close'}
