# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError, UserError
import logging
_logger = logging.getLogger(__name__)


class AqsClinicaAnamnesis(models.Model):

    _name = "aqs.clinica.anamnesis"
    _inherit = ['portal.mixin', 'mail.thread', 'mail.activity.mixin']
    _description = "Clinica Anamnesis"

    # =====================
    # GENERAL INFO FIELDS
    # =====================

    name = fields.Char(string="Numero Anamnesis", default=lambda self: self.env['ir.sequence'].next_by_code('aqs.clinica.anamnesis'))

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
            if record.patient_id:
                record.related_sales_orders = record.patient_id.sale_order_ids
            else:
                record.related_sales_orders = None

    total_sales_orders = fields.Integer(compute='_count_related_sales_orders', tracking=True, string="Total Sales Orders Project")

    # TOTAL SALES ORDERS IN PROJECT COMPUTE METHOD
    @api.depends('related_sales_orders')
    def _count_related_sales_orders(self):
        for record in self:
            if record.patient_id:
                record.total_sales_orders = len(record.related_sales_orders)
            else:
                record.total_sales_orders = None

    related_invoices = fields.One2many('account.move', string="Related Invoices", compute="_compute_related_invoices")

    @api.depends('patient_id')
    def _compute_related_invoices(self):
        for record in self:
            if record.patient_id:
                record.related_invoices = record.patient_id.invoice_ids
            else:
                record.related_invoices = None

    total_invoices = fields.Integer(compute='_count_related_invoices', tracking=True, string="Total Invoices")

    @api.depends('related_invoices')
    def _count_related_invoices(self):
        for record in self:
            if record.patient_id:
                record.total_invoices = len(record.related_invoices)
            else:
                record.total_invoices = None

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





