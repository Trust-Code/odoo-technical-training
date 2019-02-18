
import requests
import logging
from datetime import datetime
from odoo import api, fields, models
from odoo.exceptions import UserError


_logger = logging.getLogger(__name__)


class Tags(models.Model):
    _name = 'modelo.tag'

    name = fields.Char(string="Nome")


class Modelo(models.Model):
    _name = 'modelo'

    def _calcular_anos(self):
        for item in self:
            item.age = 20

    name = fields.Char(string="Nome", size=50)
    photo = fields.Binary(string="Foto")
    street = fields.Char(string="Rua", help="Rua do cliente", size=200)
    number = fields.Char(string="Número", size=10)
    age = fields.Integer(string="Idade", compute='_calcular_anos')
    is_customer = fields.Boolean(string="É cliente?")
    birth = fields.Date(string="Data de Nascimento")
    last_sale = fields.Datetime(readonly=True)

    amount_sale = fields.Float(string="Total de Vendas", default=100.0)
    gender = fields.Selection(
        [('male', 'Masculino'), ('female', 'Feminino')], string="Sexo")

    propposal_ids = fields.One2many('proposta', 'supplier_id', string="Propostas")
    tag_ids = fields.Many2many('modelo.tag', string="Marcadores")

    @api.onchange('name')
    def _onchange_name(self):
        try:
            url = 'https://api.genderize.io/?name=%s' % self.name
            resposta = requests.get(url)
            if resposta.ok:
                self.gender = resposta.json()['gender']
        except:
            _logger.warning("Não foi possível consultar genderize", exc_info=True)
            raise UserError('Não foi possível consultar, tente mais tarde')

    def action_validar_cliente(self):
        if len(self.name) < 10:
            raise UserError('Preencha o nome corretamente')

        self.last_sale = datetime.now()
