from odoo import models, fields, api
import json


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
            res_id.sudo().write({'state': 'COMPLETE'})
            submission_data = json.loads(res_id.submission_data)
            components = json.loads(self.env['formio.builder'].browse(res_id.builder_id.id).schema).get('components')
            label_list = res_id._get_label(components, submission_data, [], None)
            data = res_id._get_project_data(label_list, submission_data, [])
            return {
                "name": self.name,
                "type": "ir.actions.act_window",
                "res_model": "formio.form",
                "view_mode": "formio_form",
                "target": "new",
                "res_id": res_id.id,
                "context": {'formio_project': 1, 'data': data, 'title': opp_id.name},
            }

    def action_send_to_salesperson(self, datas, note):
        if not datas and not note:
            return
        fields_data, i = "", 1
        for data in datas:
            fields_data += f"{i}. {data.get('label', '')}: {data.get('value', '')}<br>" \
                           f"{data.get('note', '')}<br>"
            i += 1
        project = self.env['project.project'].browse(self.env.context.get('active_id'))
        content = f"You need to re-check this information: <br>{note}<br> {fields_data}"
        self.env['mail.activity'].with_user(self.env.user).create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'res_model_id': self.env.ref('crm.model_crm_lead').id,
            'res_id': project.sale_line_id.order_id.opportunity_id.id,
            'user_id': project.sale_line_id.order_id.opportunity_id.user_id.id,
            'summary': 'Sales Revision',
            'note': content,
        })
        self.env['mail.message'].create({
            'model': 'crm.lead',
            'res_id': project.sale_line_id.order_id.opportunity_id.id,
            'subject': 'Sales Revision',
            'body': content,
        })
        return True
