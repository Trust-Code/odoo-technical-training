
from odoo import fields, models
from odoo.exceptions import UserError


class Monitor(models.Model):
    _name = 'monitor'

    status = fields.Boolean(string="Status")
    hostname = fields.Char(string="Hostname")
    ip_address = fields.Char(string="Endereço IP")
    protocol = fields.Char(string="Protocolo")
    port = fields.Integer(string="Porta")

    def monitorar(self):
        import requests
        resp = requests.get(self.hostname)
        if not resp.ok:
            raise UserError('Erro no %s' % self.hostname)

    def cron_monitorar_ativos(self):
         ativo_ids = self.search([('status', '=', True)])
         for ativo in ativo_ids:
             ativo.monitorar()
