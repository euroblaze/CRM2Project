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

    def _get_project_data(self):
        self.ensure_one()
        submission_data = json.loads(self.submission_data)
        components = json.loads(self.env['formio.builder'].browse(self.builder_id.id).schema).get('components')
        label_dict = self._get_label(components)
        data = [{'key': key, 'label': label_dict[key], 'value': value} for key, value in submission_data.items() if
                label_dict.get(key)]
        return data

    def _get_label(self, components, label_dict={}):
        for component in list(filter(lambda com: com['type'] != 'button', components)):
            label_dict[component.get('key')] = component.get('label')
            if component.get('components'):
                self._get_label(components=component['components'], label_dict=label_dict)
        return label_dict
