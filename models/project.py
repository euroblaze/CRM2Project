from odoo import models, fields, api


class ProjectProject(models.Model):
    _inherit = 'project.project'

    hide_open_form_button = fields.Boolean(compute='compute_hide_open_form_button')

    @api.depends('sale_line_id')
    def compute_hide_open_form_button(self):
        val = True
        opp_id = self.sale_line_id.order_id.opportunity_id
        if opp_id and self.env['formio.form'].sudo().search([('crm_lead_id', '=', opp_id.id)], limit=1):
            val = False
        for rec in self:
            rec.hide_open_form_button = val

    def action_open_form(self):
        self.ensure_one()
        opp_id = self.sale_line_id.order_id.opportunity_id
        res_id = self.env['formio.form'].sudo().search([('crm_lead_id', '=', opp_id.id)], limit=1)
        if res_id:
            data = res_id.get_submission_data()
            return {
                "name": self.name,
                "type": "ir.actions.act_window",
                "res_model": "formio.form",
                "view_mode": "formio_form",
                "target": "new",
                "res_id": res_id.id,
                "context": {'formio_project': 1, 'data': data},
            }

    def action_send_to_salesperson(self, data, note):
        print(data)
        self.ensure_one()
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
