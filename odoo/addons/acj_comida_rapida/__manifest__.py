# -*- coding: utf-8 -*-
{
    'name': "acj_comida_rapida",

    'summary': "Gestión de un puesto de comida rápida",

    'description': """
Módulo para gestionar pedidos, productos, ingredientes y categorías en un puesto de comida rápida.
    """,

    'author': "ACJ",
    'website': "https://www.example.com",

    'category': 'Sales',
    'version': '1.0',

    'depends': ['base'],

    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',
        'views/templates.xml',
    ],
    'demo': [
        'demo/demo.xml',
    ],
}

