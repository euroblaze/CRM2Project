from odoo import fields, models


class WizardSendMessage(models.TransientModel):
    _name = "wizard.send.message"
    _description = 'Send message to salesperson'

    content = fields.Text('Content')

    def action_send(self):
        self.ensure_one()
        if not self.content:
            return
        project = self.env['project.project'].browse(self.env.context.get('active_id'))
        self.env['mail.activity'].with_user(self.env.user).create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'res_model_id': self.env.ref('crm.model_crm_lead').id,
            'res_id': project.sale_line_id.order_id.opportunity_id.id,
            'user_id': self.env.user.id,
            'summary': 'Sales Revision',
        })
        self.env['mail.message'].create({
            'model': 'crm.lead',
            'res_id': project.sale_line_id.order_id.opportunity_id.id,
            'subject': 'Sales Revision',
            'body': self.content,
        })
        return True
