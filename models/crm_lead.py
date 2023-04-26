from odoo import models, fields, _


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def action_open_form(self):
        return {
            'type': 'ir.actions.act_window',
            'name': _('Form'),
            'res_model': 'formio.form',
            'view_type': 'formio_form',
            'view_mode': 'formio_form',
            'target': 'new',
            'res_id': 3,
            'context': {'formio_form_action_draft': True},
        }
