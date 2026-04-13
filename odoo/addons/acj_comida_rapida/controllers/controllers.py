# -*- coding: utf-8 -*-
# from odoo import http


# class AcjComidaRapida(http.Controller):
#     @http.route('/acj_comida_rapida/acj_comida_rapida', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/acj_comida_rapida/acj_comida_rapida/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('acj_comida_rapida.listing', {
#             'root': '/acj_comida_rapida/acj_comida_rapida',
#             'objects': http.request.env['acj_comida_rapida.acj_comida_rapida'].search([]),
#         })

#     @http.route('/acj_comida_rapida/acj_comida_rapida/objects/<model("acj_comida_rapida.acj_comida_rapida"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('acj_comida_rapida.object', {
#             'object': obj
#         })

