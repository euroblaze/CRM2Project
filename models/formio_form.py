from odoo import api, fields, models, _
from odoo.addons.formio.models.formio_builder import STATE_CURRENT as BUILDER_STATE_CURRENT
from odoo.addons.formio.utils import get_field_selection_label
import json


class Form(models.Model):
    _inherit = 'formio.form'

    crm_lead_id = fields.Many2one('crm.lead', readonly=True, string='CRM Lead')

    def _prepare_create_vals(self, vals):
        vals = super(Form, self)._prepare_create_vals(vals)
        builder = self._get_builder_from_id(vals.get('builder_id'))
        res_id = self._context.get('active_id')

        if not builder or not builder.res_model_id.model == 'crm.lead' or not res_id:
            return vals

        lead = self.env['crm.lead'].browse(res_id)
        action = self.env.ref('crm.crm_case_tree_view_oppor')
        url = '/web?#id={id}&view_type=form&model={model}&action={action}'.format(
            id=res_id,
            model='crm.lead',
            action=action.id)
        res_model_name = builder.res_model_id.name

        vals['crm_lead_id'] = res_id
        vals['res_partner_id'] = lead.partner_id.id
        vals['res_act_window_url'] = url
        vals['res_name'] = lead.name
        return vals

    @api.onchange('builder_id')
    def _onchange_builder_domain(self):
        res = super(Form, self)._onchange_builder_domain()
        if self._context.get('active_model') == 'crm.lead':
            res_model_id = self.env.ref('crm.model_crm_lead').id
            domain = [
                ('state', '=', BUILDER_STATE_CURRENT),
                ('res_model_id', '=', res_model_id),
            ]
            res['domain'] = {'builder_id': domain}
        return res

    def get_submission_data(self):
        self.ensure_one()
        submission_data = json.loads(self.submission_data)
        schema = json.loads(self.env['formio.builder'].browse(self.builder_id.id).schema)
        data = []
        for com in schema.get('components'):
            if com['type'] != 'button':
                value = submission_data.get(com['key'])
                data.append({'key': com['key'], 'label': com['label'], 'value': value if value else False})
        return data
