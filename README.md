# 🧵 Bordados Personalizados

**Proyecto Integrador**

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

- Python 3.12 o superior
- FastAPI 
- SQLModel / Pydantic
- Persistencia: CSV
- Stripe (pagos reales)
- Desplegado en Render

## 🚀 Cómo ejecutar localmente

```bash
# 1. Clona el repositorio
git clone https://github.com/Jeff07K/Bordados_project.git
cd Bordados_project

# 2. Crea el entorno virtual (recominedo la version 3.12 de python)
python3.12 -m venv .venv
source .venv/bin/activate   # Mac/Linux
.venv\Scripts\activate      # Windows

# 2.5. Instalar los paquetes
pip install "fastapi[standard]"
pip install sqlmodel

# 3. Instala dependencias
pip install -r requirements.txt

# 4. Crea el archivo .env (copia el .env.example)
# 5. Ejecuta
uvicorn main:app --reload
```

Visita `http://127.0.0.1:8000/docs` para ver la documentación de la API.


## 👤 Autor

JEFFREY BEJARANO — Código: 67001609
