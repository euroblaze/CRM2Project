from odoo import api, fields, models, _
from odoo.exceptions import ValidationError


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    formio_forms = fields.One2many('formio.form', 'crm_lead_id', string='Forms')
    formio_forms_count = fields.Integer(
        compute='_compute_formio_forms_count', compute_sudo=True, string='Forms Count')
    formio_this_model_id = fields.Many2one(
        'ir.model', compute='_compute_formio_this_model_id', compute_sudo=True)

    def _compute_formio_forms_count(self):
        for r in self:
            r.formio_forms_count = len(r.formio_forms)

    def _compute_formio_this_model_id(self):
        self.ensure_one()
        model_id = self.env.ref('crm.model_crm_lead').id
        self.formio_this_model_id = model_id

    def write(self, vals):
        # Simpler to maintain and less risk with extending, than
        # computed field(s) in the formio.form object.
        res = super(CrmLead, self).write(vals)
        if self.formio_forms:
            form_vals = self._prepare_write_formio_form_vals(vals)
            if form_vals:
                self.formio_forms.write(form_vals)
        return res

    def _prepare_write_formio_form_vals(self, vals):
        if vals.get('name'):
            form_vals = {
                'res_name': self.name
            }
            return form_vals
        else:
            return False

    def action_formio_forms(self):
        self.ensure_one()
        res_model_id = self.env.ref('base.model_res_partner').id
        return {
            'name': 'Forms',
            'type': 'ir.actions.act_window',
            'domain': [('res_id', '=', self.id), ('res_model_id', '=', res_model_id)],
            'context': {'default_res_id': self.id},
            'view_type': 'form',
            'view_mode': 'kanban,tree,form',
            'res_model': 'formio.form',
            'view_id': False,
        }

    def action_open_form(self):
        self.ensure_one()
        show_button = True if self.order_ids.mapped('order_line.project_id') else False
        res_id = self.env['formio.form'].sudo().search([('crm_lead_id', '=', self.id)], limit=1)
        if res_id:
            res_id.sudo().write({'state': 'PENDING'})
            return {
                "name": self.name,
                "type": "ir.actions.act_window",
                "res_model": "formio.form",
                "view_mode": "formio_form",
                "target": "new",
                "res_id": res_id.id,
                "context": {'formio_crm': 1, 'show_button': show_button},
            }
        else:
            builder_id = self.env['formio.builder'].sudo().search([('res_model', '=', 'crm.lead'), ('state', '=', 'CURRENT')], limit=1)
            if not builder_id:
                raise ValidationError(_('No Form Found!'))
            values = {
                'builder_id': builder_id.id,
                'title': builder_id.title,
                'show_title': builder_id.show_form_title,
                'show_state': builder_id.show_form_state,
                'show_id': builder_id.show_form_id,
                'show_uuid': builder_id.show_form_uuid,
                'show_user_metadata': builder_id.show_form_user_metadata,
                'public_share': builder_id.public,
                'public_access_interval_number': builder_id.public_access_interval_number,
                'public_access_interval_type': builder_id.public_access_interval_type,
                'public_access_date_from': fields.Datetime.now() if builder_id.public else False,
            }
            new_form = self.env['formio.form'].with_context(
                default_res_model_id=self.formio_this_model_id,
                default_crm_lead_id=self.id,
            ).sudo().create(values)
            return {
                "name": self.name,
                "type": "ir.actions.act_window",
                "res_model": "formio.form",
                "view_mode": "formio_form",
                "target": "new",
                "res_id": new_form.id,
                "context": {'formio_crm': 1, 'show_button': show_button},
            }

    def action_send_to_pm(self):
        opp = self.env['crm.lead'].browse(self.env.context.get('active_id'))
        project = opp.order_ids.mapped('order_line.project_id')[0]
        if not project.user_id:
            raise ValidationError(_(f'No project manager found for project {project.name}'))
        self.env['mail.activity'].with_user(self.env.user).create({
            'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
            'res_model_id': self.env.ref('project.model_project_project').id,
            'res_id': project.id,
            'user_id': project.user_id.id,
            'summary': 'Check Form Information',
        })
        return True
