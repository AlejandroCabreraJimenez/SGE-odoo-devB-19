# -*- coding: utf-8 -*-

from odoo import models, fields, api


class AcjComidaRapidaOrder(models.Model):
    _name = 'acj_comida_rapida.order'
    _description = 'Pedido'

    name = fields.Char(string='Número de pedido', required=True, default='ORD001')
    date = fields.Date(string='Fecha', default=fields.Date.today)
    customer_id = fields.Many2one('res.partner', string='Cliente')
    order_line_ids = fields.One2many('acj_comida_rapida.order_line', 'order_id', string='Líneas de pedido')
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    state = fields.Selection([('draft', 'Borrador'), ('confirmed', 'Confirmado'), ('done', 'Completado'), ('cancelled', 'Cancelado')], default='draft', string='Estado')

    @api.model
    def create(self, vals):
        if vals.get('name', 'ORD001') == 'ORD001':
            vals['name'] = self.env['ir.sequence'].next_by_code('acj_comida_rapida.order') or 'ORD001'
        return super().create(vals)

    @api.depends('order_line_ids.price_subtotal')
    def _compute_total(self):
        for order in self:
            order.total = sum(line.price_subtotal for line in order.order_line_ids)

    def action_confirm(self):
        self.state = 'confirmed'

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        self.state = 'cancelled'

    def action_draft(self):
        self.state = 'draft'