# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcjComidaRapidaOrder(models.Model):
    _name = 'acj_comida_rapida.order'
    _description = 'Pedido'

    name = fields.Char(string='Número de pedido', required=True, default=lambda self: self._generate_order_number())
    date = fields.Date(string='Fecha', default=fields.Date.today)
    customer_id = fields.Many2one('res.partner', string='Cliente')
    order_line_ids = fields.One2many('acj_comida_rapida.order_line', 'order_id', string='Líneas de pedido')
    total = fields.Float(string='Total', compute='_compute_total', store=True)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_total(self):
        for order in self:
            order.total = sum(line.price_subtotal for line in order.order_line_ids)

    def _generate_order_number(self):
        return self.env['ir.sequence'].next_by_code('acj_comida_rapida.order') or 'ORD001'