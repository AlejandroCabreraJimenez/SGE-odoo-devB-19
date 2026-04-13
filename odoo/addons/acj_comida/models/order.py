# -*- coding: utf-8 -*-

from odoo import models, fields, api
from datetime import timedelta


class AcjComidaOrder(models.Model):
    _name = 'acj_comida.order'
    _description = 'Pedido'
    _sql_constraints = [
        ('positive_total', 'CHECK(total >= 0)', 'El total no puede ser negativo'),
    ]

    name = fields.Char(string='Número de Pedido', readonly=True, default=lambda self: self.env['ir.sequence'].next_by_code('acj_comida.order'))
    customer_id = fields.Many2one('res.partner', string='Cliente', required=True)
    date = fields.Datetime(string='Fecha', default=fields.Datetime.now)
    estimated_date = fields.Datetime(string='Fecha Estimada', compute='_compute_estimated_date', store=True)
    total = fields.Float(string='Total', compute='_compute_total', store=True)
    items_count = fields.Integer(string='Cantidad de Items', compute='_compute_items_count')
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

    @api.depends('date')
    def _compute_estimated_date(self):
        for order in self:
            if order.date:
                order.estimated_date = order.date + timedelta(minutes=30)
            else:
                order.estimated_date = fields.Datetime.now() + timedelta(minutes=30)

    def _compute_items_count(self):
        for order in self:
            order.items_count = sum(line.quantity for line in order.order_line_ids)

    def action_confirm(self):
        self.write({'state': 'confirmed'})

    def action_done(self):
        self.write({'state': 'done'})

    def action_cancel(self):
        self.write({'state': 'cancelled'})

    def action_draft(self):
        self.write({'state': 'draft'})

    @api.onchange('customer_id')
    def _onchange_customer(self):
        if self.customer_id and not self.order_line_ids:
            return {'warning': {
                'title': 'Nuevo Cliente',
                'message': f'Cliente {self.customer_id.name} seleccionado. No olvides agregar productos.'
            }}

    @api.model_create_multi
    def create(self, vals_list):
        orders = super().create(vals_list)
        for order in orders:
            if not order.name or order.name == 'New':
                order.name = self.env['ir.sequence'].next_by_code('acj_comida.order')
        return orders

    def write(self, vals):
        result = super().write(vals)
        if 'state' in vals and vals['state'] == 'done':
            for order in self:
                if order.total == 0:
                    raise ValidationError('No puedes confirmar un pedido sin líneas.')
        return result