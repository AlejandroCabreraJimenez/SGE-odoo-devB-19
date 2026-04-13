# -*- coding: utf-8 -*-

from odoo import models, fields


class AcjComidaCategory(models.Model):
    _name = 'acj_comida.category'
    _description = 'Categoría de Producto'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    image = fields.Binary(string='Imagen')
    active = fields.Boolean(default=True)
    product_ids = fields.One2many('acj_comida.product', 'category_id', string='Productos')