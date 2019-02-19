from odoo import fields, models


class Enrollment(models.Model):
    _name = 'school.enrollment'

    partner_id = fields.Many2one('res.partner', string="Student")

    start_date = fields.Date(string="Start Date")
    end_date = fields.Date(string="End Date")

    school_class_ids = fields.Many2many('school.class', string="Classes")

    gross_price = fields.Float(string="Base Price")
    discount = fields.Float(string="Discount (%)")
    net_price = fields.Float(string="Net Amount Monthly")
