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

    def _get_label(self, components, submission_data, label_list, parent_type):
        type_list = ['button', 'file', 'content', 'hidden', 'htmlelement', 'recaptcha', 'resource', 'nested', 'custom']
        chilren_components = {}
        for component in components:
            if component.get('type') in type_list: continue
            if parent_type in ['datagrid', 'editgrid']:
                chilren_components.update({component.get('key'): component.get('label')})
                continue
            if submission_data.get(component.get('key')) != None:
                sub_data = {}
                if component.get('type') == 'container':
                    sub_data = submission_data.get(component.get('key'))
                elif component.get('type') == 'tree':
                    sub_data = submission_data.get(component.get('key')).get('data')
                elif component.get('type') == 'currency':
                    label_list.append({
                        'key': component.get('key'),
                        'label': component.get('label'),
                        'type': component.get('type'),
                        'currency': component.get('currency'),
                        'components': self._get_label(component['components'], sub_data, [], component.get('type')) if component.get('components') else []
                    })
                    continue

                label_list.append({
                    'key': component.get('key'),
                    'label': component.get('label'),
                    'type': component.get('type'),
                    'components': self._get_label(component['components'], sub_data, [], component.get('type')) if component.get('components') else []
                })
            if component.get('type') in ['address', 'container', 'tree', 'datagrid', 'editgrid']:
                continue
            if component.get('components'):
                self._get_label(component['components'], submission_data, label_list, component.get('type'))
            elif component.get('type') == 'columns':
                for col in component['columns']:
                    self._get_label(col['components'], submission_data, label_list, component.get('type'))
            elif component.get('type') == 'table':
                for row in component['rows']:
                    for col in row:
                        self._get_label(col['components'], submission_data, label_list, component.get('type'))
        if parent_type in ['datagrid', 'editgrid']:
            return chilren_components
        return label_list

    def _add_data(self, key, label, value, type, parent_label):
        return {
            'key': key,
            'label': label,
            'value': value,
            'type': type,
            'parent_label': parent_label,
        }

    def _get_project_data(self, label_list, submission_data, data_list, parent_label=False):
        for label in label_list:
            if label['type'] not in ['container', 'tree']:
                value = submission_data[label['key']]
                if label['type'] == 'address':
                    value = submission_data[label['key']].get('display_name')
                if label['type'] in ['datagrid', 'editgrid']:
                    value = [label['components'], value]
                if label['type'] == 'currency':
                    data_list.append({
                        'key': label['key'],
                        'label': label['label'],
                        'value': value,
                        'type': label['type'],
                        'currency': label['currency'],
                        'parent_label': parent_label,
                    })
                    continue
                data_list.append(self._add_data(label['key'], label['label'], value, label['type'], parent_label))
            else:
                if label.get('components'):
                    sub_data = submission_data[label['key']] if label['type'] == 'container' else submission_data[label['key']]['data']
                    parent = label['label'] if label['type'] == 'tree' else False
                    self.get_data(label['components'], sub_data, data_list, parent)
        return data_list
