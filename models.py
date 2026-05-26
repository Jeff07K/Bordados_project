"""
models.py — Modelos SQLModel para SQLite / PostgreSQL (Supabase, Neon).
Se eliminó la persistencia CSV. Las tablas se crean automáticamente.
"""
from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime


# ─────────────────────────────────────────────────────────────────
# USUARIO
# ─────────────────────────────────────────────────────────────────

class UsuarioBase(SQLModel):
    nombre_real: str = Field(min_length=2, max_length=100)
    email: str = Field(unique=True, index=True, max_length=150)
    direccion_envio: Optional[str] = Field(default=None, max_length=300)
    activo: bool = Field(default=True)
    rol: str = Field(default="usuario")  # "usuario" | "admin"


class Usuario(UsuarioBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    contrasena_hash: str = Field(max_length=256)
    creado_en: Optional[datetime] = Field(default_factory=datetime.utcnow)


class UsuarioCreate(SQLModel):
    nombre_real: str
    email: str
    direccion_envio: Optional[str] = None
    contrasena: str  # Plano — se hashea en el router


class UsuarioUpdate(SQLModel):
    nombre_real: Optional[str] = None
    email: Optional[str] = None
    direccion_envio: Optional[str] = None
    activo: Optional[bool] = None


class UsuarioPublic(SQLModel):
    id: int
    nombre_real: str
    email: str
    direccion_envio: Optional[str]
    activo: bool
    rol: str
    creado_en: Optional[datetime]


# ─────────────────────────────────────────────────────────────────
# PRODUCTO
# ─────────────────────────────────────────────────────────────────

class ProductoBase(SQLModel):
    nombre: str = Field(min_length=2, max_length=150)
    descripcion: Optional[str] = Field(default=None, max_length=1000)
    precio: float = Field(gt=0)
    categoria: str = Field(default="bordado")  # "bordado" | "camiseta"
    stock: int = Field(default=0, ge=0)
    imagen_url: Optional[str] = Field(default=None, max_length=500)
    activo: bool = Field(default=True)


class Producto(ProductoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creado_en: Optional[datetime] = Field(default_factory=datetime.utcnow)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(SQLModel):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    precio: Optional[float] = None
    categoria: Optional[str] = None
    stock: Optional[int] = None
    imagen_url: Optional[str] = None
    activo: Optional[bool] = None


# ─────────────────────────────────────────────────────────────────
# PEDIDO PERSONALIZADO
# ─────────────────────────────────────────────────────────────────

class PedidoBase(SQLModel):
    usuario_email: str = Field(index=True, max_length=150)
    producto_id: Optional[int] = Field(default=None, foreign_key="producto.id")
    descripcion: str = Field(max_length=1000)
    talla: Optional[str] = Field(default=None, max_length=10)
    color: Optional[str] = Field(default=None, max_length=50)
    precio_estimado: Optional[float] = Field(default=None, ge=0)
    estado: str = Field(default="pendiente")
    # estados: "pendiente" | "en_proceso" | "pagado" | "cancelado"


class PedidoPersonalizado(PedidoBase, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    creado_en: Optional[datetime] = Field(default_factory=datetime.utcnow)


class PedidoCreate(PedidoBase):
    pass


class PedidoUpdate(SQLModel):
    descripcion: Optional[str] = None
    talla: Optional[str] = None
    color: Optional[str] = None
    precio_estimado: Optional[float] = None
    estado: Optional[str] = None
