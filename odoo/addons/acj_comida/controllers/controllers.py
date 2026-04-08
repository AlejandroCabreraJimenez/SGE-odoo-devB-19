# -*- coding: utf-8 -*-
# from odoo import http


# class AcjComida(http.Controller):
#     @http.route('/acj_comida/acj_comida', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/acj_comida/acj_comida/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('acj_comida.listing', {
#             'root': '/acj_comida/acj_comida',
#             'objects': http.request.env['acj_comida.acj_comida'].search([]),
#         })

#     @http.route('/acj_comida/acj_comida/objects/<model("acj_comida.acj_comida"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('acj_comida.object', {
#             'object': obj
#         })

