from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class FormBuilder(models.Model):
    _inherit = 'formio.builder'

    def _default_formio_res_model_id(self):
        return self.env.ref('CRM2Project.formio_res_model_crm_lead').id if self.env.ref('CRM2Project.formio_res_model_crm_lead') else False

    formio_res_model_id = fields.Many2one(default=_default_formio_res_model_id)
    show_form_title = fields.Boolean(default=False)
    show_form_id = fields.Boolean(default=False)
    show_form_uuid = fields.Boolean(default=False)
    show_form_state = fields.Boolean(default=False)
    wizard = fields.Boolean(default=True)

    @api.constrains('res_model')
    def _check_same_model(self):
        for rec in self:
            if self.env['formio.builder'].sudo().search([('id', '!=', rec.id), ('res_model', '=', rec.res_model)]):
                raise ValidationError(_('You can only have one form builder with model %s', rec.res_model))
