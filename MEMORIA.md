# MÓDULO ACJ COMIDA - GESTIÓN DE COMIDA RÁPIDA

## Portada

**Módulo Odoo 17 de Gestión de Comida Rápida**

**Proyecto**: 0491_SGE_RA5_Proyecto_2025-2026

**Alumno**: A.C.J.

**Módulo**: ACJ Comida

**Versión**: 1.0

**Fecha**: Abril 2026

---

## Índice

1. [Introducción](#introducción)
2. [Diagrama de Clases UML](#diagrama-de-clases-uml)
3. [Finalidad del Módulo](#finalidad-del-módulo)
4. [Funcionamiento del Módulo](#funcionamiento-del-módulo)
5. [Arquitectura Técnica](#arquitectura-técnica)
6. [Requisitos Implementados](#requisitos-implementados)
7. [Conclusiones Personales](#conclusiones-personales)
8. [Problemas Encontrados](#problemas-encontrados)
9. [Sugerencias de Mejora](#sugerencias-de-mejora)
10. [Referencias Bibliográficas](#referencias-bibliográficas)

---

## Introducción

El presente proyecto es un módulo Odoo 17 que implementa un sistema integral de gestión para restaurantes de comida rápida. El módulo "ACJ Comida" proporciona funcionalidades para la administración de productos, categorías, ingredientes, pedidos y clientes, con un enfoque en la usabilidad y la escalabilidad.

El desarrollo sigue la arquitectura MVC (Model-View-Controller) de Odoo, implementando modelos de datos robustos con validaciones tanto en Python como en SQL, vistas de usuario intuitivas y controles de seguridad granulares.

---

## Diagrama de Clases UML

```
┌─────────────────────────────────────────────────────────────────┐
│                     res.partner (heredada)                      │
├─────────────────────────────────────────────────────────────────┤
│ + id: Integer (PK)                                              │
│ + name: Char                                                    │
│ + email: Char                                                   │
│ + is_customer: Boolean                                          │
│ + phone_number: Char                                            │
│ + delivery_address: Text                                        │
│ + preferred_category: Many2one → acj_comida.category           │
├─────────────────────────────────────────────────────────────────┤
│ + total_orders(): Integer (computed)                            │
│ + total_spent(): Float (computed)                               │
│ + last_order_date(): Datetime (computed)                        │
└─────────────────────────────────────────────────────────────────┘
           △
           │ hereda
           │
┌─────────────────────────────────────────────────────────────────┐
│                   acj_comida.category                           │
├─────────────────────────────────────────────────────────────────┤
│ + id: Integer (PK)                                              │
│ + name: Char (required, unique)                                 │
│ + description: Text                                             │
│ + image: Binary                                                 │
│ + active: Boolean = True                                        │
├─────────────────────────────────────────────────────────────────┤
│ - Relación 1:N con Product                                      │
└─────────────────────────────────────────────────────────────────┘
           △
           │ 1:N
           │
┌─────────────────────────────────────────────────────────────────────┐
│                    acj_comida.product                               │
├─────────────────────────────────────────────────────────────────────┤
│ + id: Integer (PK)                                                  │
│ + name: Char (required, unique)                                     │
│ + description: Text                                                 │
│ + price: Float (required, > 0)                                      │
│ + discount: Float (0-100%) = 0.0                                    │
│ + net_price: Float (computed, stored)                               │
│ + category_id: Many2one → acj_comida.category                       │
│ + image: Binary                                                     │
│ + active: Boolean = True                                            │
│ + ingredient_ids: Many2many → acj_comida.ingredient                 │
│ + sales_count: Integer (computed)                                   │
├─────────────────────────────────────────────────────────────────────┤
│ + _check_price(): Constraint                                        │
│ + _check_discount(): Constraint                                     │
│ + _compute_net_price(): Compute field                               │
│ + _compute_sales_count(): Compute field                             │
│ + _onchange_discount(): Event handler                               │
│ - Constraints SQL: unique name, CHECK price > 0                     │
└─────────────────────────────────────────────────────────────────────┘
           △
           │ M:N
           │
┌─────────────────────────────────────────────────────────────────┐
│                 acj_comida.ingredient                           │
├─────────────────────────────────────────────────────────────────┤
│ + id: Integer (PK)                                              │
│ + name: Char (required)                                         │
│ + description: Text                                             │
│ + stock: Float                                                  │
│ + unit: Selection (kg, l, units)                                │
│ + active: Boolean = True                                        │
├─────────────────────────────────────────────────────────────────┤
│ - Relación M:N con Product                                      │
└─────────────────────────────────────────────────────────────────┘


┌──────────────────────────────────────────────────────────────────┐
│                      acj_comida.order                            │
├──────────────────────────────────────────────────────────────────┤
│ + id: Integer (PK)                                               │
│ + name: Char (readonly, sequence)                                │
│ + customer_id: Many2one → res.partner (required)                 │
│ + date: Datetime = NOW                                           │
│ + estimated_date: Datetime (computed, stored)                    │
│ + total: Float (computed, stored)                                │
│ + items_count: Integer (computed)                                │
│ + state: Selection (draft, confirmed, done, cancelled)           │
│ + order_line_ids: One2many → acj_comida.order_line               │
├──────────────────────────────────────────────────────────────────┤
│ + _compute_total(): Compute field                                │
│ + _compute_estimated_date(): Compute field                       │
│ + _compute_items_count(): Compute field                          │
│ + action_confirm(): Workflow transition                          │
│ + action_done(): Workflow transition                             │
│ + action_cancel(): Workflow transition                           │
│ + action_draft(): Workflow transition                            │
│ + _onchange_customer(): Event handler                            │
│ + create(): Override (sequence generation)                       │
│ + write(): Override (validation)                                 │
│ - Constraints SQL: CHECK total >= 0                              │
└──────────────────────────────────────────────────────────────────┘
           △
           │ 1:N
           │
┌──────────────────────────────────────────────────────────────────┐
│                   acj_comida.order_line                          │
├──────────────────────────────────────────────────────────────────┤
│ + id: Integer (PK)                                               │
│ + order_id: Many2one → acj_comida.order (required, cascade)      │
│ + product_id: Many2one → acj_comida.product (required)           │
│ + quantity: Float (required, > 0)                                │
│ + price_unit: Float (readonly, related → product.price)          │
│ + subtotal: Float (computed, stored)                             │
├──────────────────────────────────────────────────────────────────┤
│ + _compute_subtotal(): Compute field                             │
│ + _check_quantity(): Constraint                                  │
└──────────────────────────────────────────────────────────────────┘
```

---

## Finalidad del Módulo

El módulo **ACJ Comida** está diseñado para ser una solución completa de gestión operativa para restaurantes de comida rápida. Sus objetivos principales son:

### 1. **Gestión de Catálogo de Productos**
- Administración centralizada de productos disponibles
- Organización mediante categorías (hamburguesas, bebidas, acompañamientos)
- Soporte de imágenes representativas para cada producto
- Control de descuentos y cálculo automático de precios netos
- Seguimiento de ventas por producto

### 2. **Control de Inventario**
- Gestión de ingredientes con unidades de medida variables
- Registro de stock disponible
- Relación many2many entre productos e ingredientes

### 3. **Gestión de Pedidos**
- Creación y seguimiento de pedidos con workflow completo
- Estados: Borrador → Confirmado → Completado/Cancelado
- Cálculo automático de totales y cantidades
- Estimación automática de tiempo de entrega
- Edición rápida de líneas de pedido

### 4. **Gestión de Clientes**
- Extensión del modelo res.partner con información adicional
- Estadísticas de compra (total ordenado, número de órdenes)
- Categoría favorita de productos
- Dirección de entrega personalizada

### 5. **Seguridad y Permisos**
- Control granular de acceso CRUD para usuarios internos
- Permisos completos para administradores
- Separación de roles: usuarios estándar vs administradores

---

## Funcionamiento del Módulo

### Flujo de Usuario: Crear Pedido

```
1. Navega a menú "Pedidos"
   ↓
2. Crea nuevo pedido (se genera número automático)
   ↓
3. Selecciona cliente (se muestra aviso si es nuevo)
   ↓
4. Agrega líneas de pedido (edición inline):
   - Producto → Se carga automáticamente precio
   - Cantidad → Se calcula subtotal
   ↓
5. Sistema calcula automáticamente:
   - Total del pedido
   - Número de items
   - Fecha estimada de entrega
   ↓
6. Cambia estado del pedido:
   - Confirmar → Valida que tenga mínimo 1 línea
   - Completar → Marca como entregado
   - Cancelar → Rechaza la orden
```

---

## Arquitectura Técnica

### Modelos de Datos

**5 Modelos Principales:**

1. **acj_comida.category** - Categorías de productos
2. **acj_comida.product** - Productos con precios y descuentos
3. **acj_comida.ingredient** - Ingredientes con gestión de stock
4. **acj_comida.order** - Pedidos con workflow
5. **acj_comida.order_line** - Líneas de detalle de pedidos

**1 Modelo Extendido:**

6. **res.partner** - Cliente extendido con estadísticas

### Vistas Implementadas

| Modelo | Tree | Form | Kanban | Search |
|--------|------|------|--------|--------|
| Category | ✓ | ✓ | - | - |
| Product | ✓ | ✓ | ✓ | - |
| Ingredient | ✓ | ✓ | - | - |
| Order | ✓ | ✓ | ✓ | ✓ |
| OrderLine | Inline | - | - | - |

---

## Requisitos Implementados

### ✅ Requisitos Mínimos (5 puntos)

- [x] **4+ clases en ficheros diferentes**: 5 clases + 1 extendida
- [x] **Relaciones (one2many, many2one, many2many)**: Todas implementadas
- [x] **Vistas Form y Tree**: Para cada modelo
- [x] **Campos en vistas**: Todos los campos utilizados
- [x] **Imágenes representativas**: Binary fields en Category, Product
- [x] **Menús y submenús**: 1 menú raíz + 4 submenús
- [x] **Seguridad básica**: CRUD parcial/completo
- [x] **Icono del módulo**: Personalizado
- [x] **Demo data**: Categorías, productos, ingredientes, órdenes

### ✅ Requisitos Adicionales (6 PAP)

1. Campos computados complejos (net_price, sales_count, estimated_date)
2. Eventos onchange (discount warning, customer notification)
3. Lógica create/write (sequence generation, validation)
4. Constraints SQL y Python
5. Vista Kanban compleja para Order
6. Herencia de res.partner

---

## Conclusiones

El módulo implementa exitosamente un sistema profesional de gestión para comida rápida, cumpliendo todos los requisitos mínimos y varios adicionales que demuestran dominio de la arquitectura Odoo.

---

## Referencias

- Odoo 17 Developer Documentation
- Odoo Source Code Repository
- Estándares de codificación Python (PEP 8)
- Documentación de PostgreSQL

---

**Fin de Memoria**

*Documento generado: Abril 2026*
*Módulo ACJ Comida v1.0*
