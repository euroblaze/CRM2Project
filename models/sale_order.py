from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('project_id', 'opportunity_id')
    def _check_same_project_and_opp(self):
        for rec in self:
            if self.env['sale.order'].sudo().search([('id', '!=', rec.id),
                                                     ('opportunity_id', '=', rec.opportunity_id.id),
                                                     ('project_id', '=', rec.project_id.id)]):
                raise ValidationError(_("A project can't link to multiple opportunity!"))
