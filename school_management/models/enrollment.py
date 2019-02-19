from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
    _name = 'school.enrollment'

    partner_id = fields.Many2one('res.partner', string="Student")

    start_date = fields.Date(string="Start Date", required=True)
    end_date = fields.Date(string="End Date", required=True)

    school_class_ids = fields.Many2many('school.class', string="Classes")

    gross_price = fields.Float(string="Base Price")
    discount = fields.Float(string="Discount (%)")
    net_price = fields.Float(string="Net Amount Monthly")

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_date_intervals(self):
        start = fields.Date.from_string(self.start_date)
        end = fields.Date.from_string(self.end_date)
        if start >= end:
            raise ValidationError("Data final deve ser maior que data inicial")
