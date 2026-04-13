# -*- coding: utf-8 -*-

from odoo import models, fields


class AcjComidaRapidaCategory(models.Model):
    _name = 'acj_comida_rapida.category'
    _description = 'Categoría de productos'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')