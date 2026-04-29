# 🧵 Bordados Personalizados

**Proyecto Integrador — FastAPI · CRUD · CSV · 2026-1**

Plataforma web para la gestión y venta de bordados artesanales personalizados.

## 🎯 Descripción del proyecto

Tienda en línea que ofrece:
- Catálogo de bordados y camisetas con bordado
- Sistema de pedidos personalizados
- Registro y autenticación de usuarios
- Pago con tarjeta (integración Stripe)

## 🗂️ Modelos de datos

| Modelo | Descripción |
|--------|-------------|
| `Usuario` | Clientes: nombre, email, dirección, contraseña, activo |
| `Producto` | Artículos del catálogo: nombre, precio, categoría, stock, activo |
| `PedidoPersonalizado` | Solicitudes: descripción, talla, color, precio estimado, estado |

## ⚙️ Tecnologías

- Python 3.11
- FastAPI 0.135
- SQLModel / Pydantic
- Persistencia: CSV
- Stripe (pagos reales)
- Desplegado en Render

## 🚀 Cómo ejecutar localmente

```bash
# 1. Clona el repositorio
git clone https://github.com/TU_USUARIO/bordados-personalizados.git
cd bordados-personalizados

# 2. Crea el entorno virtual
python -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Crea el archivo .env (copia el .env.example)
# 5. Ejecuta
uvicorn main:app --reload
```

Visita `http://127.0.0.1:8000/docs` para ver la documentación de la API.

## 📋 Endpoints principales

Ver tabla completa en [GUIA_MAESTRA.md](GUIA_MAESTRA.md)

## 👤 Autor

**Tu Nombre Completo** — Código: XXXXXXXX
