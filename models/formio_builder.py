from odoo import models, fields


class FormBuilder(models.Model):
    _inherit = 'formio.builder'

    def _default_formio_res_model_id(self):
        return self.env.ref('CRM2Project.formio_res_model_crm_lead').id if self.env.ref('CRM2Project.formio_res_model_crm_lead') else False

    formio_res_model_id = fields.Many2one(default=_default_formio_res_model_id)
