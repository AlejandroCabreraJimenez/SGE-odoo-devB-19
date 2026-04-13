# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcjComidaRapidaProduct(models.Model):
    _name = 'acj_comida_rapida.product'
    _description = 'Producto'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    price = fields.Float(string='Precio', required=True)
    category_id = fields.Many2one('acj_comida_rapida.category', string='Categoría')
    ingredient_ids = fields.Many2many('acj_comida_rapida.ingredient', string='Ingredientes')
    image = fields.Binary(string='Imagen')
    ingredient_count = fields.Integer(string='Número de ingredientes', compute='_compute_ingredient_count')

    @api.depends('ingredient_ids')
    def _compute_ingredient_count(self):
        for product in self:
            product.ingredient_count = len(product.ingredient_ids)

    @api.constrains('price')
    def _check_price(self):
        for record in self:
            if record.price <= 0:
                raise ValidationError("El precio debe ser positivo.")