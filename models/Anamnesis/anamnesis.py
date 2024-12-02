# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError, UserError
import uuid
import werkzeug
from dateutil.relativedelta import relativedelta
import datetime
import base64
from babel.dates import format_date
import pytz
import zipfile
from io import BytesIO
import time
import logging
_logger = logging.getLogger(__name__)


class AqsClinicaAnamnesis(models.Model):

    _name = "aqs.clinica.anamnesis"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Clinica Anamnesis"

    # =====================
    # GENERAL INFO FIELDS
    # =====================

    name = fields.Char(string="Numero Anamnesis")

    patient_id = fields.Many2one('res.partner', string="Patient", tracking=True)
    doctor_id = fields.Many2one('res.users', string="Doctor", tracking=True)

    historial_medico_personal = fields.Text(string="Historial Medico Personal")
    historial_medico_familiar = fields.Text(string="Historial Medico Familiar")
    motivo_de_consulta = fields.Text(string="Motivo de Consulta")
    enfermedad_actual = fields.Char(string="Enfermedad Actual")
    examen_fisico = fields.Text(string="Examen Fisico")
    res_de_pruebas_diag = fields.Text(string="Resultados de Pruebas Diagnosticas")
    diagnostico = fields.Char(string="Diagnostico")
    plan_de_tratamiento = fields.Text(string="Plan de Tratamiento")
    ev_notas_prog = fields.Text(string="Evolucion y notas de progreso")

    related_sales_orders = fields.One2many('sale.order', string="Related Sales Orders", compute="_compute_related_sales_orders")

    @api.depends('patient_id')
    def _compute_related_sales_orders(self):
        for record in self:
            record.related_sales_orders = self.env['sale.order'].search([('partner_id', '=', record.patient_id.id)])

    total_sales_orders_in_project = fields.Integer(compute='_count_related_sales_orders', store=True, tracking=True, string="Total Sales Orders Project")

    # TOTAL SALES ORDERS IN PROJECT COMPUTE METHOD
    @api.depends('related_sales_orders')
    def _count_related_sales_orders(self):
        for record in self:
            record.total_sales_orders_in_project = len(record.related_sales_orders)

    related_invoices = fields.One2many('account.move', string="Related Invoices", compute="_compute_related_invoices")

    @api.depends('patient_id')
    def _compute_related_invoices(self):
        for record in self:
            record.related_invoices = self.env['account.move'].search([('partner_id', '=', record.patient_id.id), ('move_type', 'in', ['out_invoice', 'out_refund'])])

    total_invoices = fields.Integer(compute='_count_related_invoices', store=True, tracking=True, string="Total Invoices")

    @api.depends('related_invoices')
    def _count_related_invoices(self):
        for record in self:
            record.total_invoices = len(record.related_invoices)

    def action_sales_orders(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Sales Orders',
            'res_model': 'sale.order',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.patient_id.id)],
        }

    def action_invoices(self):
        return {
            'type': 'ir.actions.act_window',
            'name': 'Invoices',
            'res_model': 'account.move',
            'view_mode': 'tree,form',
            'domain': [('partner_id', '=', self.patient_id.id)],
        }





