from datetime import date, timedelta
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class Enrollment(models.Model):
    _name = 'school.enrollment'
    _order = 'id desc'

    _inherit = ['mail.activity.mixin', 'mail.thread']

    def _default_company_id(self):
        return self.env.user.company_id

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    @api.multi
    def name_get(self):
        result = []
        for record in self:
            name = '[%s] %s' % (record.code or '', record.partner_id.name)
            result.append((record.id, name))
        return result

    def _compute_invoice_count(self):
        for enrollment in self:
            total = self.env['account.invoice'].search_count(
                [('origin_enrollment_id', '=', enrollment.id)])
            enrollment.invoice_count = total

    invoice_count = fields.Integer(compute='_compute_invoice_count')

    company_id = fields.Many2one(
        'res.company', string="Company", required=True, readonly=True,
        states={'draft': [('readonly', False)]}, default=_default_company_id)

    partner_id = fields.Many2one(
        'res.partner', string="Student", required=True, readonly=True,
        states={'draft': [('readonly', False)]})

    code = fields.Char(string="Code")
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
        string="State", default="draft", readonly=True, copy=False,
        track_visibility='onchange')

    origin_order_id = fields.Many2one('sale.order')
    next_invoice = fields.Date(string="Next Invoice")

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
        sequence = self.env.ref('school_management.sequence_enrollment')
        code = sequence.next_by_id()
        self.write({'state': 'in_use', 'code': code})

    def action_expiry(self):
        self.write({'state': 'expired'})

    def action_back_draft(self):
        self.write({'state': 'draft'})

    @api.model
    def create(self, vals):
        vals['next_invoice'] = vals['start_date']
        return super(Enrollment, self).create(vals)

    def generate_invoices(self):
        enrollment_ids = self.search([('state', '=', 'in_use'),
                                      ('next_invoice', '<=', date.today())])

        for enrollment in enrollment_ids:

            lista = [(0, False, {
                'product_id': x.product_id.id,
                'name': x.name,
                'quantity': 1,
                'price_unit': x.total_price,
                'account_id': x.product_id.categ_id.property_account_income_categ_id.id,
            }) for x in enrollment.school_class_ids]

            self.env['account.invoice'].create({
                'partner_id': enrollment.partner_id.id,
                'company_id': enrollment.company_id.id,
                'origin': enrollment.code,
                'type': 'out_invoice',
                'date_invoice': date.today(),
                'invoice_line_ids': lista,
                'origin_enrollment_id': enrollment.id,
            })

            enrollment.next_invoice = date.today() + timedelta(days=30)

    def action_view_invoices(self):
        action = self.env.ref('account.action_invoice_tree1').read()[0]

        invoice_ids = self.env['account.invoice'].search(
            [('origin_enrollment_id', '=', self.id)])

        action['domain'] = [('id', 'in', invoice_ids.ids)]
        return action

    def cron_expiry_enrollments(self):
        enrollment_ids = self.search([('state', '=', 'in_use'),
                                      ('end_date', '<=', date.today())])
        enrollment_ids.action_expiry()
