from odoo import fields, models, api


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char('Patient Name', required=True, tracking=True)
    date_of_birth = fields.Date(string='DOB', required=True)
    gender= fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    tag_ids = fields.Many2many('patient.tag', 'patient_tag_rel', 'tag_id', string="Tags")
