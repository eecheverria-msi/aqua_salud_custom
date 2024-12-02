from odoo import api, exceptions, fields, models, _
from datetime import date
from datetime import datetime, time
from time import strptime
from dateutil.relativedelta import relativedelta
from odoo.exceptions import AccessError, UserError, ValidationError


class AquaSaludResPartner(models.Model):
    _inherit = "res.partner"

    birth_date = fields.Date(string="Birth Date", tracking=True)
    document_type = fields.Selection([
        ('DNI', 'DNI'),
        ('Pasaporte', 'Pasaporte'),
        ('NIE', 'NIE'),], string="Document Type", tracking=True)
    document_number = fields.Char(string="Document Number", tracking=True)
    marital_status = fields.Selection([
        ('Casado', 'Casado'),
        ('Soltero', 'Soltero'),
        ('Separado', 'Separado'),
        ('Divorciado', 'Divorciado'),
        ('Viudo', 'Viudo'),], string="Marital Status", tracking=True)