from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pydantic import BaseModel
import stripe
import os

from db import init_all_csv
from models import (
    UsuarioCreate, UsuarioUpdate,
    ProductoCreate, ProductoUpdate,
    PedidoPersonalizadoCreate, PedidoPersonalizadoUpdate,
)
from operations_csv import (
    createUsuario, findAllUsuarios, findOneUsuario, findUsuarioByEmail, updateUsuario, killUsuario,
    createProducto, findAllProductos, findOneProducto, findProductosByCategoria, findProductosByNombre, updateProducto, killProducto,
    createPedido, findAllPedidos, findOnePedido, findPedidosByEstado, findPedidosByEmail, updatePedido, killPedido,
)

stripe.api_key = os.environ.get("STRIPE_SECRET_KEY", "")

class PagoRequest(BaseModel):
    monto: float
    descripcion: str

@asynccontextmanager
async def lifespan(app: FastAPI):
    init_all_csv()
    yield

app = FastAPI(
    title="Bordados Personalizados API",
    description="""
## API de Bordados Personalizados — v1.8 CSV
Proyecto Integrador 

### Modelos (los 3 solicita la encuesta :3)
- **Usuario** — clientes de la tienda
- **Producto** — bordados y camisetas del catálogo
- **PedidoPersonalizado** — solicitudes personalizadas

### Funcionalidades extra
- Filtro por atributo (categoría, estado)
- Búsqueda por atributo ≠ ID (email, nombre)
- Soft delete con histórico (campo `activo` / `estado`)
- Pago real con Stripe
    """,
    version="1.0.0",
    lifespan=lifespan,
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/", include_in_schema=False)
async def root():
    return FileResponse("static/index.html")

# ── PAGO ─────────────────────────────────────────────────────────────────────
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

# ══════════════════════════════════════════════════════════════════
#  USUARIO
# ══════════════════════════════════════════════════════════════════

@app.post("/usuario", status_code=201, tags=["Usuario"])
async def create_usuario(data: UsuarioCreate):
    return createUsuario(data)

@app.get("/usuario", tags=["Usuario"])
async def find_all_usuarios(solo_activos: bool = Query(False, description="Mostrar solo usuarios activos")):
    """Retorna todos los usuarios"""
    return findAllUsuarios(solo_activos)

@app.get("/usuario/buscar", tags=["Usuario"])
async def buscar_usuario_por_email(email: str = Query(..., description="Email del usuario a buscar")):
    """Búsqca por atributo, no es lo mismo que ID: busca usuario por email."""
    resultado = findUsuarioByEmail(email)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"No se encontró usuario con email: {email}")
    return resultado

@app.get("/usuario/{usuario_id}", tags=["Usuario"])
async def find_one_usuario(usuario_id: int):
    u = findOneUsuario(usuario_id)
    if not u:
        raise HTTPException(status_code=404, detail=f"{usuario_id} Usuario no encontrado")
    return u

@app.patch("/usuario/{usuario_id}", tags=["Usuario"])
async def update_usuario(usuario_id: int, data: UsuarioUpdate):
    u = updateUsuario(usuario_id, data)
    if not u:
        raise HTTPException(status_code=404, detail=f"{usuario_id} Usuario no encontrado")
    return u

@app.delete("/usuario/{usuario_id}", tags=["Usuario"])
async def kill_usuario(usuario_id: int):
    """" Estado de usuario , activo o no  """
    d = killUsuario(usuario_id)
    if not d:
        raise HTTPException(status_code=404, detail=f"{usuario_id} Usuario no encontrado")
    return {"mensaje": "Usuario inactivado (histórico conservado)", "usuario": d}

# ══════════════════════════════════════════════════════════════════
#  PRODUCTO
# ══════════════════════════════════════════════════════════════════

@app.post("/producto", status_code=201, tags=["Producto"])
async def create_producto(data: ProductoCreate):
    return createProducto(data)

@app.get("/producto", tags=["Producto"])
async def find_all_productos(solo_activos: bool = Query(False)):
    return findAllProductos(solo_activos)

@app.get("/producto/filtrar/categoria", tags=["Producto"])
async def filtrar_productos_por_categoria(categoria: str = Query(..., description="Ej: bordado, camiseta")):
    """istado filtrado."""
    resultado = findProductosByCategoria(categoria)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"No hay productos con categoría: {categoria}")
    return resultado

@app.get("/producto/buscar/nombre", tags=["Producto"])
async def buscar_producto_por_nombre(nombre: str = Query(..., description="Nombre o parte del nombre")):
    """Búsqca por atributo, no es lo mismo que ID:"""
    resultado = findProductosByNombre(nombre)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"No se encontraron productos con nombre: {nombre}")
    return resultado

@app.get("/producto/{producto_id}", tags=["Producto"])
async def find_one_producto(producto_id: int):
    p = findOneProducto(producto_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"{producto_id} Producto no encontrado")
    return p

@app.patch("/producto/{producto_id}", tags=["Producto"])
async def update_producto(producto_id: int, data: ProductoUpdate):
    p = updateProducto(producto_id, data)
    if not p:
        raise HTTPException(status_code=404, detail=f"{producto_id} Producto no encontrado")
    return p

@app.delete("/producto/{producto_id}", tags=["Producto"])
async def kill_producto(producto_id: int):
    """el producto se marca como inactivo."""
    d = killProducto(producto_id)
    if not d:
        raise HTTPException(status_code=404, detail=f"{producto_id} Producto no encontrado")
    return {"mensaje": "Producto inactivado (histórico conservado)", "producto": d}

# ══════════════════════════════════════════════════════════════════
#  PEDIDO PERSONALIZADO
# ══════════════════════════════════════════════════════════════════

@app.post("/pedido", status_code=201, tags=["Pedido"])
async def create_pedido(data: PedidoPersonalizadoCreate):
    return createPedido(data)

@app.get("/pedido", tags=["Pedido"])
async def find_all_pedidos():
    return findAllPedidos()

@app.get("/pedido/filtrar/estado", tags=["Pedido"])
async def filtrar_pedidos_por_estado(estado: str = Query(..., description="pendiente | en_proceso | pagado | cancelado")):
    """Filtro por estado."""
    resultado = findPedidosByEstado(estado)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"No hay pedidos con estado: {estado}")
    return resultado

@app.get("/pedido/buscar/email", tags=["Pedido"])
async def buscar_pedidos_por_email(email: str = Query(..., description="Email del cliente")):
    """Búsqueda por email (atributo ≠ ID)."""
    resultado = findPedidosByEmail(email)
    if not resultado:
        raise HTTPException(status_code=404, detail=f"No hay pedidos para: {email}")
    return resultado

@app.get("/pedido/{pedido_id}", tags=["Pedido"])
async def find_one_pedido(pedido_id: int):
    p = findOnePedido(pedido_id)
    if not p:
        raise HTTPException(status_code=404, detail=f"{pedido_id} Pedido no encontrado")
    return p

@app.patch("/pedido/{pedido_id}", tags=["Pedido"])
async def update_pedido(pedido_id: int, data: PedidoPersonalizadoUpdate):
    p = updatePedido(pedido_id, data)
    if not p:
        raise HTTPException(status_code=404, detail=f"{pedido_id} Pedido no encontrado")
    return p

@app.delete("/pedido/{pedido_id}", tags=["Pedido"])
async def kill_pedido(pedido_id: int):
    """ cambia estado a 'cancelado', conserva el registro."""
    d = killPedido(pedido_id)
    if not d:
        raise HTTPException(status_code=404, detail=f"{pedido_id} Pedido no encontrado")
    return {"mensaje": "Pedido cancelado (histórico conservado)", "pedido": d}