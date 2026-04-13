# -*- coding: utf-8 -*-

from odoo import models, fields


class AcjComidaRapidaIngredient(models.Model):
    _name = 'acj_comida_rapida.ingredient'
    _description = 'Ingrediente'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    price = fields.Float(string='Precio')