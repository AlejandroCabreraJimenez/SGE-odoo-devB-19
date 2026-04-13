# -*- coding: utf-8 -*-

from odoo import models, fields, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_customer = fields.Boolean(string='Es Cliente', default=True)
    phone_number = fields.Char(string='Teléfono')
    delivery_address = fields.Text(string='Dirección de Entrega')
    total_orders = fields.Integer(string='Total de Pedidos', compute='_compute_total_orders')
    total_spent = fields.Float(string='Total Gastado', compute='_compute_total_spent')
    preferred_category = fields.Many2one('acj_comida.category', string='Categoría Favorita')
    last_order_date = fields.Datetime(string='Última Orden', compute='_compute_last_order_date')

    def _compute_total_orders(self):
        for partner in self:
            partner.total_orders = self.env['acj_comida.order'].search_count([
                ('customer_id', '=', partner.id)
            ])

    def _compute_total_spent(self):
        for partner in self:
            orders = self.env['acj_comida.order'].search([
                ('customer_id', '=', partner.id),
                ('state', '=', 'done')
            ])
            partner.total_spent = sum(order.total for order in orders)

    def _compute_last_order_date(self):
        for partner in self:
            last_order = self.env['acj_comida.order'].search([
                ('customer_id', '=', partner.id)
            ], order='date desc', limit=1)
            partner.last_order_date = last_order.date if last_order else False
