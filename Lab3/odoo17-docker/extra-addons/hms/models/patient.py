from odoo import models, fields, api
from datetime import date
from odoo.exceptions import ValidationError


class HmsPatient(models.Model):
    _name = 'hms.patient'
    _inherit = ['mail.thread', 'mail.activity.mixin']
    _description = 'Hospital Patient'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)

    birth_date = fields.Date()
    age = fields.Integer(compute="_compute_age", store=True)

    image = fields.Binary()
    address = fields.Text()
    history = fields.Html()

    blood_type = fields.Selection([
        ('a', 'A'),
        ('b', 'B'),
        ('ab', 'AB'),
        ('o', 'O')
    ])

    pcr = fields.Boolean()
    cr_ratio = fields.Float()

    state = fields.Selection([
        ('undetermined', 'Undetermined'),
        ('good', 'Good'),
        ('fair', 'Fair'),
        ('serious', 'Serious')
    ], default='undetermined', tracking=True)

    department_id = fields.Many2one('hms.department')
    doctor_id = fields.Many2one('hms.doctor', string="Doctor", ondelete='restrict')


    department_capacity = fields.Integer(
        related='department_id.capacity',
        store=True
    )

    # ⭐ NEW FIELDS FOR ODOO 17 UI LOGIC
    is_department_selected = fields.Boolean(compute="_compute_flags")
    is_old_patient = fields.Boolean(compute="_compute_flags")

    # =====================
    # COMPUTE
    # =====================
    @api.depends('birth_date', 'department_id', 'age')
    def _compute_flags(self):
        for rec in self:
            rec.is_department_selected = bool(rec.department_id)
            rec.is_old_patient = rec.age >= 50

    @api.depends('birth_date')
    def _compute_age(self):
        for rec in self:
            if rec.birth_date:
                today = date.today()
                rec.age = today.year - rec.birth_date.year - ((today.month, today.day) < (rec.birth_date.month, rec.birth_date.day))
            else:
                rec.age = 0

    @api.constrains('department_id')
    def _check_department(self):
        for rec in self:
            if rec.department_id and not rec.department_id.is_opened:
                raise ValidationError("You cannot select a closed department")

    @api.constrains('pcr', 'cr_ratio')
    def _check_pcr(self):
        for rec in self:
            if rec.pcr and not rec.cr_ratio:
                raise ValidationError("CR ratio is required when PCR is checked")
