
from odoo import fields, models

class SchoolEnrollment(models.Model):
    _inherit = 'school.enrollment'

    last_invoice = fields.Date(string="Last Invoice")
