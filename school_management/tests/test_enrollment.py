
from odoo.tests.common import TransactionCase
from odoo.exceptions import ValidationError


class TestEnrollment(TransactionCase):

    def setUp(self):
        super(TestEnrollment, self).setUp()
        self.geografia = self.env['school.class'].create({
            'name': 'Geografia',
            'starting_hour': 15,
            'ending_hour': 18,
            'hour_price': 12.0,
        })
        self.matematica = self.env['school.class'].create({
            'name': 'Matematica',
            'starting_hour': 8,
            'ending_hour': 11,
            'hour_price': 20.0,
        })
        self.aluno = self.env['res.partner'].create({
            'name': 'Aluno'
        })
        self.enrollment = self.env['school.enrollment'].create({
            'partner_id': self.aluno.id,
            'start_date': '2019-02-01',
            'end_date': '2019-02-11',
            'discount': 5,
            'school_class_ids': [(4, self.geografia.id, False),
                                 (4, self.matematica.id, False)]
        })


    def test_total_prices(self):
        self.assertEqual(len(self.enrollment.school_class_ids), 2)
        self.assertEqual(self.geografia.total_hours, 3)
        self.assertEqual(self.geografia.total_price, 36)
        self.assertEqual(self.enrollment.net_price, 91.2)

    def test_constrains(self):
        with self.assertRaises(ValidationError):
            self.env['school.class'].create({
                'name': 'Matematica',
                'starting_hour': 11,
                'ending_hour': 8,
                'hour_price': 20.0,
            })

        with self.assertRaises(ValidationError):
            self.env['school.enrollment'].create({
                'partner_id': self.aluno.id,
                'start_date': '2019-02-11',
                'end_date': '2019-02-02',
                'discount': 5,
            })

    def test_enrollment_flow(self):
        self.assertEqual(self.enrollment.state, 'draft')

        self.enrollment.action_confirm()
        self.assertEqual(self.enrollment.state, 'in_use')

        self.enrollment.action_expiry()
        self.assertEqual(self.enrollment.state, 'expired')

        self.enrollment.action_back_draft()
        self.assertEqual(self.enrollment.state, 'draft')
