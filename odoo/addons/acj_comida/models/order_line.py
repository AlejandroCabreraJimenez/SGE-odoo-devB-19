# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class AcjComidaOrderLine(models.Model):
    _name = 'acj_comida.order_line'
    _description = 'Línea de Pedido'

    order_id = fields.Many2one('acj_comida.order', string='Pedido', required=True, ondelete='cascade')
    product_id = fields.Many2one('acj_comida.product', string='Producto', required=True)
    quantity = fields.Float(string='Cantidad', default=1.0, required=True)
    price_unit = fields.Float(string='Precio Unitario', related='product_id.price', readonly=True)
    subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.subtotal = line.quantity * line.price_unit

    @api.constrains('quantity')
    def _check_quantity(self):
        for line in self:
            if line.quantity <= 0:
                raise ValidationError('La cantidad debe ser mayor que cero.')