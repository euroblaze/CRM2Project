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
            return {
                "name": self.name,
                "type": "ir.actions.act_window",
                "res_model": "formio.form",
                "view_mode": "formio_form",
                "target": "new",
                "res_id": res_id.id,
            }
