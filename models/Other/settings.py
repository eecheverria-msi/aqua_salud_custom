# -*- coding: utf-8 -*-

from odoo import models, fields, api, tools
from odoo.tools.translate import _
from odoo.exceptions import UserError
from odoo.exceptions import ValidationError, UserError
import uuid
import werkzeug
import json

class ClinicaSettings(models.TransientModel):
    _inherit = 'res.config.settings'



