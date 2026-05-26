"""
main.py — Bordados Personalizados API v2.0
Base de datos: SQLite local / Supabase / Neon (configurable via DATABASE_URL)
"""
from contextlib import asynccontextmanager
import os
import stripe
from fastapi import FastAPI, HTTPException, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel

from db import init_db
from routers import auth_router, productos, pedidos, usuarios


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    yield


stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

app = FastAPI(
    title="🧵 Bordados Personalizados API",
    description="""
## API de Bordados Personalizados — v2.0

### Mejoras v2.0
- ✅ **SQLite** local (sin configuración)
- ✅ **Supabase / Neon** en producción (solo cambiar `DATABASE_URL`)
- ✅ **Autenticación JWT** con roles usuario/admin
- ✅ **Frontend** separado en 4 páginas

### Modelos
- **Usuario** — clientes y administradores
- **Producto** — catálogo de bordados y camisetas
- **PedidoPersonalizado** — solicitudes personalizadas con estado

### Deploy en Render
Variables de entorno necesarias:
- `DATABASE_URL` — Neon o Supabase PostgreSQL URL
- `SECRET_KEY` — Clave secreta JWT
- `STRIPE_SECRET_KEY` / `STRIPE_PUBLISHABLE_KEY`
""",
    version="2.0.0",
    lifespan=lifespan,
)

# ── Routers ───────────────────────────────────────────────────────
app.include_router(auth_router.router)
app.include_router(productos.router)
app.include_router(pedidos.router)
app.include_router(usuarios.router)

# ── Static files ──────────────────────────────────────────────────
app.mount("/static", StaticFiles(directory="static"), name="static")


# ── Páginas HTML ──────────────────────────────────────────────────
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


@app.get("/admin", include_in_schema=False)
async def admin_page():
    return FileResponse("static/admin.html")


# ── Stripe ────────────────────────────────────────────────────────
class PagoRequest(BaseModel):
    monto: float
    descripcion: str


@app.get("/pago/config", tags=["Pago"])
async def stripe_config():
    return {"publishable_key": os.environ.get("STRIPE_PUBLISHABLE_KEY", "")}


@app.post("/pago/crear-intent", tags=["Pago"])
async def crear_payment_intent(data: PagoRequest):
    if not stripe.api_key:
        raise HTTPException(status_code=500, detail="STRIPE_SECRET_KEY no configurado")
    try:
        intent = stripe.PaymentIntent.create(
            amount=int(data.monto * 100),
            currency="usd",
            description=data.descripcion,
            automatic_payment_methods={"enabled": True},
        )
        return {"client_secret": intent.client_secret}
    except stripe.StripeError as e:
        raise HTTPException(status_code=400, detail=str(e))
