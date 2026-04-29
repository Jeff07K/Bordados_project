from sqlmodel import SQLModel, Field


# ─────────────────────────────────────────────
#  USUARIO
# ─────────────────────────────────────────────

class UsuarioBase(SQLModel):
    nombre_real:     str | None = Field(default=None, nullable=True)
    email:           str | None = Field(default=None, nullable=True)
    direccion_envio: str | None = Field(default=None, nullable=True)
    contrasena:      str | None = Field(default=None, nullable=True)
    activo:          bool       = Field(default=True)  # histórico: True=activo, False=inactivo


class Usuario(UsuarioBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class UsuarioCreate(UsuarioBase):
    pass


class UsuarioUpdate(UsuarioBase):
    pass


# ─────────────────────────────────────────────
#  PRODUCTO
# ─────────────────────────────────────────────

class ProductoBase(SQLModel):
    nombre:      str   | None = Field(default=None, nullable=True)
    descripcion: str   | None = Field(default=None, nullable=True)
    precio:      float | None = Field(default=None, nullable=True)
    categoria:   str   | None = Field(default=None, nullable=True)  # "bordado" | "camiseta"
    stock:       int   | None = Field(default=None, nullable=True)
    activo:      bool         = Field(default=True)  # histórico


class Producto(ProductoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class ProductoCreate(ProductoBase):
    pass


class ProductoUpdate(ProductoBase):
    pass


# ─────────────────────────────────────────────
#  PEDIDO PERSONALIZADO
# ─────────────────────────────────────────────

class PedidoPersonalizadoBase(SQLModel):
    usuario_email:   str   | None = Field(default=None, nullable=True)
    producto_id:     int   | None = Field(default=None, nullable=True)
    descripcion:     str   | None = Field(default=None, nullable=True)
    talla:           str   | None = Field(default=None, nullable=True)
    color:           str   | None = Field(default=None, nullable=True)
    precio_estimado: float | None = Field(default=None, nullable=True)
    estado:          str   | None = Field(default="pendiente", nullable=True)
    # estado funciona como histórico: "pendiente" | "en_proceso" | "pagado" | "cancelado"


class PedidoPersonalizado(PedidoPersonalizadoBase, table=True):
    id: int | None = Field(default=None, primary_key=True)


class PedidoPersonalizadoCreate(PedidoPersonalizadoBase):
    pass


class PedidoPersonalizadoUpdate(PedidoPersonalizadoBase):
    pass
