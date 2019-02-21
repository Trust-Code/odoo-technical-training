from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
    _name = 'school.enrollment'

    _inherit = ['mail.activity.mixin', 'mail.thread']

    def _default_company_id(self):
        return self.env.user.company_id

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = '%s - %s até %s' % (record.partner_id.name,
                                       record.start_date, record.end_date)
            result.append((record.id, name))
        return result

    company_id = fields.Many2one(
        'res.company', string="Company", required=True, readonly=True,
        states={'draft': [('readonly', False)]}, default=_default_company_id)

    partner_id = fields.Many2one(
        'res.partner', string="Student", required=True, readonly=True,
        states={'draft': [('readonly', False)]})

    start_date = fields.Date(string="Start Date", required=True, readonly=True,
                             states={'draft': [('readonly', False)]})
    end_date = fields.Date(string="End Date", required=True, readonly=True,
                           states={'draft': [('readonly', False)]})

    school_class_ids = fields.Many2many(
        'school.class', string="Classes", readonly=True,
        states={'draft': [('readonly', False)]})

    currency_id = fields.Many2one(
        'res.currency', string="Moeda",default=_default_currency_id,
        readonly=True, states={'draft': [('readonly', False)]})
    gross_price = fields.Monetary(
        string="Base Price", compute="_compute_price", store=True)
    discount = fields.Float(string="Discount (%)", readonly=True,
                            states={'draft': [('readonly', False)]})
    net_price = fields.Monetary(string="Net Amount Monthly",
                                compute='_compute_final_value', store=True)
    state = fields.Selection(
        [('draft', 'Draft'), ('in_use', 'In Use'), ('expired', 'Expired')],
        string="State", default="draft", readonly=True, copy=False)

    @api.one
    @api.constrains('start_date', 'end_date')
    def _check_date_intervals(self):
        start = fields.Date.from_string(self.start_date)
        end = fields.Date.from_string(self.end_date)
        if start >= end:
            raise ValidationError("Data final deve ser maior que data inicial")

    @api.depends('school_class_ids')
    def _compute_price(self):
        for item in self:
            item.gross_price = sum(line.total_price for line in item.school_class_ids)

    @api.depends('discount', 'gross_price')
    def _compute_final_value(self):
        for item in self:
            item.net_price = item.gross_price * (1 - (item.discount / 100))

    def action_confirm(self):
        self.write({'state': 'in_use'})

    def action_expiry(self):
        self.write({'state': 'expired'})

    def action_back_draft(self):
        self.write({'state': 'draft'})
