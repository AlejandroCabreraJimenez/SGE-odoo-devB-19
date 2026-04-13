# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcjComidaRapidaOrderLine(models.Model):
    _name = 'acj_comida_rapida.order_line'
    _description = 'Línea de pedido'

    order_id = fields.Many2one('acj_comida_rapida.order', string='Pedido')
    product_id = fields.Many2one('acj_comida_rapida.product', string='Producto', required=True)
    quantity = fields.Integer(string='Cantidad', default=1, required=True)
    price_unit = fields.Float(string='Precio unitario', related='product_id.price', readonly=True)
    price_subtotal = fields.Float(string='Subtotal', compute='_compute_subtotal', store=True)

    @api.depends('quantity', 'price_unit')
    def _compute_subtotal(self):
        for line in self:
            line.price_subtotal = line.quantity * line.price_unit