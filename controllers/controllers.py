# -*- coding: utf-8 -*-
# from odoo import http


# class /var/lib/odoo/addons/18.0/gestionNominas(http.Controller):
#     @http.route('//var/lib/odoo/addons/18.0/gestion_nominas//var/lib/odoo/addons/18.0/gestion_nominas', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('//var/lib/odoo/addons/18.0/gestion_nominas//var/lib/odoo/addons/18.0/gestion_nominas/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('/var/lib/odoo/addons/18.0/gestion_nominas.listing', {
#             'root': '//var/lib/odoo/addons/18.0/gestion_nominas//var/lib/odoo/addons/18.0/gestion_nominas',
#             'objects': http.request.env['/var/lib/odoo/addons/18.0/gestion_nominas./var/lib/odoo/addons/18.0/gestion_nominas'].search([]),
#         })

#     @http.route('//var/lib/odoo/addons/18.0/gestion_nominas//var/lib/odoo/addons/18.0/gestion_nominas/objects/<model("/var/lib/odoo/addons/18.0/gestion_nominas./var/lib/odoo/addons/18.0/gestion_nominas"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('/var/lib/odoo/addons/18.0/gestion_nominas.object', {
#             'object': obj
#         })

