from odoo import fields, models, api, _
from odoo.exceptions import ValidationError, UserError


class HospitalPatient(models.Model):
    _name = 'hospital.patient'
    _inherit = ['mail.thread']
    _description = 'Patient Master'

    name = fields.Char('Patient Name', required=True, tracking=True)
    date_of_birth = fields.Date(string='DOB', required=True)
    gender= fields.Selection([('male', 'Male'), ('female', 'Female')], string="Gender")
    tag_ids = fields.Many2many('patient.tag', 'patient_tag_rel', 'tag_id', string="Tags")
    is_minor = fields.Boolean(string="Minor")
    guardian = fields.Char(string="Guardian")
    weight = fields.Float(string="Weight")

    @api.ondelete(at_uninstall=False)
    def _check_patient_appointment(self):
        for rec in self:
            domain = [('patient_id', '=', rec.id)]
            appointments = self.env['hospital.appointment'].search(domain)
            if appointments:
                raise UserError(
                    _("You cannot delete the patient now."
                      "\nAppointments existing for this patient"))