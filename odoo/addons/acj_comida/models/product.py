# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcjComidaProduct(models.Model):
    _name = 'acj_comida.product'
    _description = 'Producto de Comida'

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    price = fields.Float(string='Precio', required=True)
    category_id = fields.Many2one('acj_comida.category', string='Categoría')
    image = fields.Binary(string='Imagen')
    active = fields.Boolean(default=True)
    ingredient_ids = fields.Many2many('acj_comida.ingredient', string='Ingredientes')

    @api.constrains('price')
    def _check_price(self):
        for product in self:
            if product.price <= 0:
                raise ValidationError('El precio debe ser mayor que cero.')