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
- Organización mediante categorías (hamburguesas, bebidas, acompañamientos, etc.)
- Soporte de imágenes representativas para cada producto
- Control de descuentos y cálculo automático de precios netos
- Seguimiento de ventas por producto

### 2. **Control de Inventario**
- Gestión de ingredientes con unidades de medida variables
- Registro de stock disponible
- Relación many2many entre productos e ingredientes
- Base para futuros sistemas de control de existencias

### 3. **Gestión de Pedidos**
- Creación y seguimiento de pedidos con workflow completo
- Estados: Borrador → Confirmado → Completado/Cancelado
- Cálculo automático de totales y cantidades
- Estimación automática de tiempo de entrega
- Edición rápida de líneas de pedido (inline editing)

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

### Flujo de Usuario: Cliente Nuevo

```
1. Accede al módulo ACJ Comida
   ↓
2. Visualiza productos en vista KANBAN (con imágenes)
   ↓
3. Busca productos usando filtros y búsqueda avanzada
   ↓
4. Consulta detalles de categorías e ingredientes
```

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
   - Confirmar → Válida que tenga mínimo 1 línea
   - Completar → Marca como entregado
   - Cancelar → Rechaza la orden
```

### Flujo de Usuario: Administrador

```
Acceso completo a:
├─ Crear/Editar/Eliminar todas las entidades
├─ Modificar precios, descuentos
├─ Gestionar inventario de ingredientes
├─ Crear categorías
└─ Ver reportes y estadísticas (futuro)
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

### Relaciones entre Modelos

```
res.partner ──1:N──→ acj_comida.order
                    ├─1:N─→ acj_comida.order_line
                    │       └─N:1─→ acj_comida.product
                    │               ├─N:1─→ acj_comida.category
                    │               └─N:M─→ acj_comida.ingredient
                    │
                    └─N:1─→ acj_comida.category (preferred)
```

### Vistas Implementadas

| Modelo | Tree | Form | Kanban | Search |
|--------|------|------|--------|--------|
| Category | ✓ | ✓ | - | - |
| Product | ✓ | ✓ | ✓ | - |
| Ingredient | ✓ | ✓ | - | - |
| Order | ✓ | ✓ | ✓ | ✓ |
| OrderLine | Inline | - | - | - |

### Características de Seguridad

- Permisos CRUD diferenciados por grupo
- Grupo de usuarios internos: lectura, creación, edición (sin eliminar)
- Grupo de administradores: lectura, creación, edición, eliminar
- Protección de campos críticos (readonly en ciertos contextos)

### Validaciones Implementadas

**Validaciones Python:**
- Precio debe ser > 0 (Product)
- Descuento entre 0-100% (Product)
- Cantidad > 0 (OrderLine)
- Nombre único (Product)

**Validaciones SQL:**
- Constraint: nombre único en products
- Constraint: precio > 0
- Constraint: total >= 0 en orders

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
- [x] **Icono del módulo**: Pollo frito personalizado
- [x] **Demo data**: Categorías, productos, ingredientes, órdenes

### ✅ Requisitos Adicionales (hasta 5 PAP = 2.5 puntos)

1. **Campos computados complejos** (1 PAP)
   - `Product.net_price` (depende de precio y descuento)
   - `Product.sales_count` (relación inversa)
   - `Order.estimated_date` (datetime + timedelta)
   - `Order.items_count` (suma de líneas)

2. **Eventos onchange** (1 PAP)
   - `Product._onchange_discount()` (aviso si > 50%)
   - `Order._onchange_customer()` (aviso nuevo cliente)

3. **Lógica sobre eventos create/write** (1 PAP)
   - `Order.create()` override para secuencia
   - `Order.write()` override para validaciones

4. **Constraints SQL y Python** (1 PAP)
   - SQL: unique names, CHECK constraints
   - Python: @api.constrains decorators

5. **Vista Kanban compleja** (1 PAP)
   - Order Kanban agrupada por estado
   - Con campos múltiples, colores destacados

6. **Herencia de modelo existente** (1 PAP)
   - `res.partner` extendido con campos propios
   - Campos computados que relacionan con órdenes

**Total: 6 PAP implementados**

---

## Conclusiones Personales

Este proyecto ha proporcionado una experiencia integral en el desarrollo de módulos Odoo profesionales. Las conclusiones son:

### Aspectos Positivos

1. **Arquitectura Escalable**: El diseño permite fácil expansión con nuevas funcionalidades (reportes, wizards, etc.)

2. **Seguridad Robusta**: La implementación de dos niveles de validación (Python + SQL) garantiza integridad de datos.

3. **UX Intuitiva**: Las vistas Kanban y búsquedas avanzadas hacen el módulo fácil de usar.

4. **Reutilización de Código**: La herencia de res.partner demuestra la potencia de la arquitectura Odoo.

5. **Documentación Clara**: El código está bien comentado y tiene estructura coherente.

### Aprendizajes Clave

- Dominio de la arquitectura MVC de Odoo
- Implementación correcta de relaciones (Many2one, One2many, Many2many)
- Uso de decoradores @api.depends, @api.constrains, @api.onchange
- Seguridad y control de acceso en Odoo
- Vistas XML avanzadas (Kanban, búsqueda, tree, form)
- Extensión de modelos existentes mediante herencia

---

## Problemas Encontrados

### 1. **Sincronización de Secuencias** (Resuelto)
**Problema**: El número de pedido no se generaba correctamente en algunos casos.
**Solución**: Override del método `create()` para asegurar generación de secuencia.

### 2. **Validación Circular** (Prevenido)
**Problema**: Riesgo de validar total vacío al crear líneas de pedido.
**Solución**: Implementar validación en `write()` método, no en create.

### 3. **Performance en Campos Computados** (Optimizado)
**Problema**: `sales_count` podría ser lento con muchos registros.
**Solu**: Usar `search()` con domain en lugar de filtrar en Python.
Futuro: Implementar índices SQL.

### 4. **Cascada de Eliminación** (Configurado)
**Problema**: Eliminar order debería eliminar order_lines.
**Solución**: `ondelete='cascade'` en Many2one hacia order.

### 5. **Mostrar Aviso en Onchange** (Implementado)
**Problema**: Usuarios no sabían cuándo había un descuento alto.
**Solución**: Implementar `_onchange_discount()` con return warning.

---

## Sugerencias de Mejora

### Corto Plazo (MVP+)

1. **Reportes y Análisis**
   - Reporte de ventas por product
   - Reporte de pedidos por cliente
   - Gráfico de ventas por categoría

2. **Wizards**
   - Wizard para creación rápida de categorías
   - Wizard para importar productos en lote

3. **Notificaciones**
   - Email cuando estado de pedido cambia
   - Alertas de bajo stock de ingredientes

### Mediano Plazo

4. **Gestión Avanzada de Pedidos**
   - Asignación a repartidores
   - Tracking en tiempo real
   - Historial de cambios (chatter)

5. **Mejoras de Pricing**
   - Promociones por categoría
   - Ofertas por cantidad (volume pricing)
   - Combos de productos

6. **Integración**
   - POS (Point of Sale)
   - E-commerce
   - APIs REST

### Largo Plazo

7. **Inteligencia de Negocio**
   - Predicción de demanda (ML)
   - Optimización de inventario
   - Recomendaciones personalizadas

8. **Experiencia del Usuario**
   - App móvil nativa
   - Portal de clientes
   - Gamificación (puntos, logros)

---

## Referencias Bibliográficas

### Documentación Oficial

1. Odoo 17 Developer Documentation
   - https://www.odoo.com/documentation/17.0/
   - Models, Fields, Views, ORM API

2. Odoo Source Code Repository
   - https://github.com/odoo/odoo
   - v17.0 branch

### Libros y Guías

3. "Mastering Odoo" by Parth Gajjar
   - Arquitectura avanzada de módulos
   - Patrones de desarrollo Odoo

4. "Odoo Development Cookbook" by Holger Brunn
   - Recetas y best practices
   - Solución de problemas comunes

### Estándares y Patrones

5. PEP 8 - Python Enhancement Proposal
   - Estilo de código Python
   - https://www.python.org/dev/peps/pep-0008/

6. Odoo Coding Standards
   - Naming conventions
   - Module structure guidelines

### Herramientas

7. PostgreSQL 12+ Documentation
   - Constraints SQL
   - Indexing y performance

8. XML Schema Definition
   - View definitions en Odoo

---

## Información Técnica Adicional

### Estructura de Directorios

```
acj_comida/
├── __init__.py              # Importación de modelos
├── __manifest__.py          # Metadatos del módulo
├── controllers/
│   ├── __init__.py
│   └── controllers.py       # Controladores HTTP (vacio)
├── data/
│   └── sequences.xml        # Secuencias (números pedidos)
├── demo/
│   └── demo.xml            # Datos de demostración
├── models/
│   ├── __init__.py
│   ├── category.py         # Categoría
│   ├── ingredient.py       # Ingrediente
│   ├── order.py            # Pedido
│   ├── order_line.py       # Línea de pedido
│   ├── product.py          # Producto
│   └── res_partner.py      # Extensión de cliente
├── security/
│   └── ir.model.access.csv # Permisos CRUD
├── static/
│   └── description/
│       └── icon.png        # Icono del módulo
└── views/
    ├── category_views.xml       # Vistas de categoría
    ├── ingredient_views.xml     # Vistas de ingrediente
    ├── menus.xml               # Menús y acciones
    ├── order_line_views.xml    # Vistas de línea
    ├── order_views.xml         # Vistas de pedido
    ├── product_views.xml       # Vistas de producto
    ├── templates.xml           # Templates (vacío)
    └── views.xml               # Views generales (vacío)
```

### Dependencias

- **Odoo 17.0**
- **Python 3.10+**
- **PostgreSQL 12+**
- **base** (módulo core de Odoo)

### Secuencias

- **acj_comida.order** - Generador de números de pedido (formato: PED0001, PED0002, etc.)

---

**Fin de Memoria**

*Documento generado: Abril 2026*
*Módulo ACJ Comida v1.0*
*Versión completa con requisitos mínimos + 6 requisitos adicionales*
