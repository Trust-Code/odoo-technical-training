
from odoo import fields, models


class ResPartner(models.Model):
    _inherit = 'res.partner'

    student = fields.Boolean(string="Student")
    teacher = fields.Boolean(string="Teacher")
