# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcjComidaProduct(models.Model):
    _name = 'acj_comida.product'
    _description = 'Producto de Comida'
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'El nombre del producto debe ser único'),
        ('price_positive', 'CHECK(price > 0)', 'El precio debe ser mayor que cero'),
    ]

    name = fields.Char(string='Nombre', required=True)
    description = fields.Text(string='Descripción')
    price = fields.Float(string='Precio', required=True)
    discount = fields.Float(string='Descuento %', default=0.0)
    net_price = fields.Float(string='Precio Neto', compute='_compute_net_price', store=True)
    category_id = fields.Many2one('acj_comida.category', string='Categoría')
    image = fields.Binary(string='Imagen')
    active = fields.Boolean(default=True)
    ingredient_ids = fields.Many2many('acj_comida.ingredient', string='Ingredientes')
    sales_count = fields.Integer(string='Cantidad Vendida', compute='_compute_sales_count')

    @api.constrains('price')
    def _check_price(self):
        for product in self:
            if product.price <= 0:
                raise ValidationError('El precio debe ser mayor que cero.')

    @api.constrains('discount')
    def _check_discount(self):
        for product in self:
            if product.discount < 0 or product.discount > 100:
                raise ValidationError('El descuento debe estar entre 0 y 100%.')

    @api.depends('price', 'discount')
    def _compute_net_price(self):
        for product in self:
            product.net_price = product.price * (1 - product.discount / 100)

    def _compute_sales_count(self):
        for product in self:
            product.sales_count = sum(self.env['acj_comida.order_line'].search([
                ('product_id', '=', product.id)
            ]).mapped('quantity'))

    @api.onchange('discount')
    def _onchange_discount(self):
        if self.discount > 50:
            return {'warning': {
                'title': 'Descuento Alto',
                'message': 'El descuento es muy alto (>50%). Verifica que sea correcto.'
            }}