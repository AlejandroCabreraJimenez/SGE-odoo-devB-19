# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcjComidaOrder(models.Model):
    _name = 'acj_comida.order'
    _description = 'Pedido'

    name = fields.Char(string='Número de Pedido', readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('acj_comida.order'))
    customer_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    state = fields.Selection([
        ('draft', 'Borrador'),
        ('confirmed', 'Confirmado'),
        ('done', 'Hecho'),
        ('cancelled', 'Cancelado'),
    ], string='Estado', default='draft')
    order_line_ids = fields.One2many('acj_comida.order_line', 'order_id', string='Líneas de Pedido')

    @api.depends('order_line_ids.subtotal')
    def _compute_total(self):
        for order in self:
            order.total = sum(line.subtotal for line in order.order_line_ids)