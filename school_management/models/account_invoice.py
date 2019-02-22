
from odoo import fields, models


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    origin_enrollment_id = fields.Many2one('school.enrollment')
