# 🧵 Bordados Personalizados — v 0.2.0 
solo funciona en local por ahora 

Tienda online de bordados pedidos personalizados.


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
