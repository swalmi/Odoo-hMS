from odoo import models, fields, api
from odoo.exceptions import ValidationError

class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'
    _rec_name = 'name'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)
    name = fields.Char(compute='_compute_name', store=True)

    image = fields.Binary()

    department_id = fields.Many2one('hms.department')
    patient_ids = fields.One2many('hms.patient', 'doctor_id', string="Patients")

    @api.depends('first_name', 'last_name')
    def _compute_name(self):
        for rec in self:
            rec.name = f"{rec.first_name} {rec.last_name}"

    def unlink(self):
        for rec in self:
            if rec.patient_ids:
                raise ValidationError("You cannot delete a doctor who has patients assigned!")
        return super(HmsDoctor, self).unlink()


