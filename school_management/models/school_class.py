
from odoo import api, fields, models
from odoo.exceptions import ValidationError


class SchoolClass(models.Model):
    _name = 'school.class'

    name = fields.Char(string="Name", size=100)
    weekday = fields.Selection(
        [('monday', 'Monday'),
         ('tuesday', 'Tuesday'),
         ('wednesday', 'Wednesday'),
         ('thursday', 'Thursday'),
         ('friday', 'Friday Yey')], string="Week Day")
    starting_hour = fields.Float(string="Starting Hour", required=True)
    ending_hour = fields.Float(string="Ending Hour", required=True)

    partner_id = fields.Many2one('res.partner', string="Professor")
    hour_price = fields.Float(string="Price per Hour")

    total_price = fields.Float(string="Total Price")

    @api.one
    @api.constrains('starting_hour', 'ending_hour')
    def _check_description(self):
        if self.ending_hour <= self.starting_hour:
            raise ValidationError("Hora Final deve ser maior que hora inicial")
