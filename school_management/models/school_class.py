
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolClass(models.Model):
    _name = 'school.class'

    def _default_currency_id(self):
        return self.env.user.company_id.currency_id

    active = fields.Boolean(string="Active", default=True)
    name = fields.Char(string="Name", size=100)
    weekday = fields.Selection(
        [('monday', 'Monday'),
         ('tuesday', 'Tuesday'),
         ('wednesday', 'Wednesday'),
         ('thursday', 'Thursday'),
         ('friday', 'Friday Yey')], string="Week Day")
    starting_hour = fields.Float(string="Starting Hour", required=True)
    ending_hour = fields.Float(string="Ending Hour", required=True)
    total_hours = fields.Float(
        string="Total Hours", compute='_compute_total_hours', store=True)

    partner_id = fields.Many2one('res.partner', string="Professor")

    currency_id = fields.Many2one('res.currency', string="Moeda",
                                  default=_default_currency_id)
    hour_price = fields.Monetary(string="Price per Hour")

    total_price = fields.Monetary(
        string="Total Price", compute='_compute_total_price', store=True)

    @api.one
    @api.constrains('starting_hour', 'ending_hour')
    def _check_description(self):
        if self.ending_hour <= self.starting_hour:
            raise ValidationError("Hora Final deve ser maior que hora inicial")

    @api.depends('starting_hour', 'ending_hour')
    def _compute_total_hours(self):
        for item in self:
            item.total_hours = item.ending_hour - item.starting_hour

    @api.depends('total_hours', 'hour_price')
    def _compute_total_price(self):
        for item in self:
            item.total_price = item.total_hours * item.hour_price
