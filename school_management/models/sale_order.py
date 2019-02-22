from datetime import date, timedelta
from odoo import api, fields, models


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    def _compute_enrollment_count(self):
        for order in self:
            total = self.env['school.enrollment'].search_count(
                [('origin_order_id', '=', order.id)])
            order.enrollment_count = total

    enrollment_count = fields.Integer(compute='_compute_enrollment_count')

    def action_view_enrollments(self):
        action = self.env.ref('school_management.action_school_enrollment').read()[0]
        enrollment = self.env['school.enrollment'].search(
            [('origin_order_id', '=', self.id)])

        action['views'] = [(self.env.ref('school_management.view_school_enrollment_form').id, 'form')]
        action['res_id'] = enrollment.id
        return action

    @api.multi
    def action_confirm(self):
        res = super(SaleOrder, self).action_confirm()
        for order in self:
            aulas = self.env['school.class']

            for line in order.order_line:

                aula = self.env['school.class'].search([('product_id', '=', line.product_id.id)])
                aulas |= aula

            triplets = []
            for aula in aulas:
                triplets.append((4, aula.id, None))

            enrollment = self.env['school.enrollment'].create({
                'start_date': date.today(),
                'end_date': date.today() + timedelta(days=365),
                'partner_id': order.partner_id.id,
                'company_id': order.company_id.id,
                'currency_id': order.pricelist_id.currency_id.id,
                'school_class_ids': triplets,
                'origin_order_id': order.id,
            })
            enrollment.message_post(
                'This enrollment was created from <a href=# data-oe-model=sale.order data-oe-id=%d>%s</a>' % (order.id, order.name))

        return res
