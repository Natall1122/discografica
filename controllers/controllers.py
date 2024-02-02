# -*- coding: utf-8 -*-
# from odoo import http


# class Discografica(http.Controller):
#     @http.route('/discografica/discografica', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/discografica/discografica/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('discografica.listing', {
#             'root': '/discografica/discografica',
#             'objects': http.request.env['discografica.discografica'].search([]),
#         })

#     @http.route('/discografica/discografica/objects/<model("discografica.discografica"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('discografica.object', {
#             'object': obj
#         })
