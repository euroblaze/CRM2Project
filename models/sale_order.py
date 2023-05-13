from odoo import models, fields, api, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    @api.constrains('project_id', 'opportunity_id')
    def _check_same_project_and_opp(self):
        for rec in self:
            if self.sudo().search([('opportunity_id', '!=', rec.opportunity_id.id),
                                   ('order_line.project_id', 'in', rec.order_line.mapped('project_id').ids)]):
                raise ValidationError(_("A project can't link to multiple opportunity!"))
