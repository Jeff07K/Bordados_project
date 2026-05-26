# 🧵 Bordados Personalizados — v2.0

Tienda online de bordados artesanales con sistema de pedidos personalizados.

## ✨ Novedades v2.0

- **SQLite** local → **Supabase / Neon** en producción (solo cambiar `DATABASE_URL`)
- **Autenticación JWT** con roles usuario/admin
- **4 páginas HTML** separadas con CSS y JS propios
- API organizada en **routers** por módulo

## 🗂️ Estructura

```
Bordados_project/
├── main.py              ← FastAPI app + rutas de páginas
├── db.py                ← Conexión SQLite / Supabase / Neon
├── models.py            ← Modelos SQLModel
├── auth.py              ← JWT + hashing
├── routers/
│   ├── auth_router.py   ← POST /auth/register, /auth/login
│   ├── productos.py     ← CRUD /producto/
│   ├── pedidos.py       ← CRUD /pedido/
│   └── usuarios.py      ← CRUD /usuario/
└── static/
    ├── index.html       ← Catálogo público
    ├── login.html       ← Inicio de sesión
    ← register.html     ← Registro
    ├── dashboard.html   ← Panel del usuario
    ├── admin.html       ← Panel administrador
    ├── css/main.css     ← Estilos globales
    └── js/api.js        ← Capa de llamadas a la API
```


## 👤 Autor

Jeffrey Bejarano
