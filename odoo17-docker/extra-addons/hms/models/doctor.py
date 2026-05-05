from odoo import models, fields

class HmsDoctor(models.Model):
    _name = 'hms.doctor'
    _description = 'Hospital Doctor'

    first_name = fields.Char(required=True)
    last_name = fields.Char(required=True)

    image = fields.Binary()

    department_id = fields.Many2one('hms.department')
    patient_ids = fields.Many2many('hms.patient', string="Patients")
