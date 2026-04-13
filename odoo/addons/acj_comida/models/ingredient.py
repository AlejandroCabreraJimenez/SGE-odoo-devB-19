# -*- coding: utf-8 -*-

from odoo import models, fields


class AcjComidaIngredient(models.Model):
    _name = 'acj_comida.ingredient'
    _description = 'Ingrediente'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    stock = fields.Float(string='Stock')
    unit = fields.Selection([
        ('kg', 'Kilogramos'),
        ('l', 'Litros'),
        ('units', 'Unidades'),
    ], string='Unidad', required=True)
    active = fields.Boolean(default=True)