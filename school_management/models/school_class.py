
from odoo import fields, models


class SchoolClass(models.Model):
    _name = 'school.class'

    name = fields.Char(string="Name", size=100)
    weekday = fields.Selection(
        [('monday', 'Monday'),
         ('tuesday', 'Tuesday'),
         ('wednesday', 'Wednesday'),
         ('thursday', 'Thursday'),
         ('friday', 'Friday Yey')], string="Week Day")
    starting_hour = fields.Float(string="Starting Hour")
    ending_hour = fields.Float(string="Ending Hour")

    partner_id = fields.Many2one('res.partner', string="Professor")
    hour_price = fields.Float(string="Price per Hour")

    total_price = fields.Float(string="Total Price")
