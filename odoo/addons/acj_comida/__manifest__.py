# -*- coding: utf-8 -*-
{
    'name': "ACJ Comida",

    'summary': "Gestión de Comida Rápida",

    'description': """
Módulo para gestionar menús, pedidos, inventario y categorías en un restaurante de comida rápida.
Permite crear productos, gestionar pedidos de clientes, controlar ingredientes y organizar por categorías.
    """,

    'author': "ACJ",
    'website': "https://www.yourcompany.com",

    'category': 'Services',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/category_views.xml',
        'views/product_views.xml',
        'views/ingredient_views.xml',
        'views/order_views.xml',
        'views/order_line_views.xml',
        'views/menus.xml',
        'data/sequences.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
    'installable': True,
    'application': True,
    'icon': '/acj_comida/static/description/icon.png',
}

