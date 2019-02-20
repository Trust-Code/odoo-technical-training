from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
    _name = 'school.enrollment'

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    partner_id = fields.Many2one('res.partner', string="Student")

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    school_class_ids = fields.Many2many('school.class', string="Classes")

    currency_id = fields.Many2one('res.currency', string="Moeda",
                                   default=_default_currency_id)
    gross_price = fields.Monetary(
        string="Base Price", compute="_compute_price", store=True)
    discount = fields.Float(string="Discount (%)")
    net_price = fields.Monetary(string="Net Amount Monthly",
                             compute='_compute_final_value', store=True)

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_date_intervals(self):
        start = fields.Date.from_string(self.start_date)
        end = fields.Date.from_string(self.end_date)
        if start >= end:
            raise ValidationError("Data final deve ser maior que data inicial")

    @api.depends('school_class_ids')
    def _compute_price(self):
        import ipdb; ipdb.set_trace()
        for item in self:
            item.gross_price = sum(line.total_price for line in item.school_class_ids)

    @api.depends('discount', 'gross_price')
    def _compute_final_value(self):
        for item in self:
            item.net_price = item.gross_price * (1 - (item.discount / 100))
