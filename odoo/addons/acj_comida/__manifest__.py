# -*- coding: utf-8 -*-
{
    'name': "ACJ Comida",

    'summary': "Gestión de Comida Rápida",

    'description': """
Módulo profesional para gestionar menús, pedidos, inventario y categorías en un restaurante de comida rápida.
Permite crear productos con descuentos, gestionar pedidos de clientes con seguimiento de estado,
controlar ingredientes y organizar productos por categorías.

Características principales:
- Gestión completa de productos con precios y descuentos
- Sistema de categorías para organizar productos
- Control de inventario de ingredientes
- Gestión de pedidos con seguimiento de estado
- Información extendida de clientes (estadísticas de compra)
- Vistas Kanban complejas para visualización ágil
- Búsquedas avanzadas con filtros
    """,

    'author': "ACJ",
    'website': "https://www.yourcompany.com",

    'category': 'Services',
    'version': '1.0',

    'depends': ['base', 'web'],

    'data': [
        'security/ir.model.access.csv',
        'data/sequences.xml',
        'views/category_views.xml',
        'views/product_views.xml',
        'views/ingredient_views.xml',
        'views/order_views.xml',
        'views/res_partner_views.xml',
        'views/order_line_views.xml',
        'views/menus.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'icon': '/acj_comida/static/description/icon.png',
    'license': 'LGPL-3',
}

