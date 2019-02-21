from odoo import http
from odoo.http import request

class EnrollmentController(http.Controller):

    @http.route(['/my/enrollments'], type='http', auth='user',
                methods=['GET'], website=True)
    def list_enrollments(self, **kwargs):
        partner = request.env.user.partner_id
        enrollments = request.env['school.enrollment'].search(
            [('partner_id', '=', partner.id)])
        values = {
            "enrollments": enrollments,
            "total": 15,
        }
        return request.render(
            'school_management.list_enrollment_template', values)


    @http.route(['/my/enrollment/<model("school.enrollment"):enrollment_id>'],
                type='http', auth='user', methods=['GET'], website=True)
    def view_enrollment(self, enrollment_id):
        values = {
            'doc': enrollment_id,
        }
        return request.render(
            'school_management.view_enrollment_template', values)
