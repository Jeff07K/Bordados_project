"""
main.py — Bordados Personalizados API v2.0
Base de datos: SQLite local / Neon PostgreSQL (configurable)
"""

from contextlib import asynccontextmanager
import os
import stripe
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from fastapi.middleware.cors import CORSMiddleware

# Importar base de datos y routers
from db import init_db
from routers import auth_router, productos, pedidos, usuarios


# ==================== LIFESPAN ====================
@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()          # Inicializa las tablas
    print("✅ Base de datos inicializada correctamente")
    yield


# ==================== STRIPE ====================
stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")


# ==================== CREACIÓN DE LA APP ====================
app = FastAPI(
    title="🧵 Bordados Personalizados API",
    description="""
    ### API para tienda de bordados personalizados
    """,
    version="2.0.0",
    lifespan=lifespan,
)

# ==================== CORS (IMPORTANTE) ====================
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],           # Cambiar a dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ==================== ROUTERS ====================
app.include_router(auth_router.router)
app.include_router(productos.router)
app.include_router(pedidos.router)
app.include_router(usuarios.router)

# ==================== STATIC FILES ====================
app.mount("/static", StaticFiles(directory="static"), name="static")


# ==================== PÁGINAS HTML ====================
@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("static/index.html")


@app.get("/login", include_in_schema=False)
async def login_page():
    return FileResponse("static/login.html")


@app.get("/register", include_in_schema=False)
async def register_page():
    return FileResponse("static/register.html")


@app.get("/dashboard", include_in_schema=False)
async def dashboard_page():
    return FileResponse("static/dashboard.html")


# ==================== HEALTH CHECK ====================
@app.get("/health")
def health():
    return {"status": "ok", "message": "API funcionando correctamente"}