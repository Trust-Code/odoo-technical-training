from odoo import fields, models


class Proposta(models.Model):
    _name = 'proposta'

    name = fields.Char(string="Referência")
    supplier_id = fields.Many2one('modelo', string="Fornecedor")

    amount = fields.Float(string="Total")
