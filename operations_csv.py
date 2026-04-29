"""
operations_csv.py
F.U.C.K. sobre archivos CSV  (Find · Update · Create · Kill)
+ endpoints de filtro y búsqueda por atributo (criterios 6 y 7 del formulario)
"""

import csv
import os
from models import (
    UsuarioCreate, UsuarioUpdate,
    ProductoCreate, ProductoUpdate,
    PedidoPersonalizadoCreate, PedidoPersonalizadoUpdate,
)
from db import (
    USUARIOS_CSV,  USUARIOS_FIELDS,
    PRODUCTOS_CSV, PRODUCTOS_FIELDS,
    PEDIDOS_CSV,   PEDIDOS_FIELDS,
)


# ════════════════════════════════════════════════════════════════════════
#  UTILIDADES GENÉRICAS
# ════════════════════════════════════════════════════════════════════════

def _read_all(filepath: str, fields: list[str]) -> list[dict]:
    if not os.path.exists(filepath):
        return []
    with open(filepath, "r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f, fieldnames=fields))


def _write_all(filepath: str, fields: list[str], rows: list[dict]) -> None:
    with open(filepath, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def _next_id(rows: list[dict]) -> int:
    if len(rows) <= 1:
        return 1
    ids = [int(r["id"]) for r in rows[1:] if r.get("id", "").isdigit()]
    return max(ids) + 1 if ids else 1


# ════════════════════════════════════════════════════════════════════════
#  USUARIO
# ════════════════════════════════════════════════════════════════════════

def createUsuario(data: UsuarioCreate) -> dict:
    rows = _read_all(USUARIOS_CSV, USUARIOS_FIELDS)
    new_id = _next_id(rows)
    new_row = {"id": new_id, **data.model_dump()}
    with open(USUARIOS_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=USUARIOS_FIELDS).writerow(new_row)
    return new_row


def findAllUsuarios(solo_activos: bool = False) -> list[dict]:
    rows = _read_all(USUARIOS_CSV, USUARIOS_FIELDS)
    data = rows[1:]
    if solo_activos:
        data = [r for r in data if r.get("activo", "True") == "True"]
    return data


def findOneUsuario(usuario_id: int) -> dict | None:
    for row in findAllUsuarios():
        if row["id"] == str(usuario_id):
            return row
    return None


# ─── CRITERIO 7: búsqueda por email (atributo ≠ ID) ──────────────────────
def findUsuarioByEmail(email: str) -> list[dict]:
    return [r for r in findAllUsuarios() if r.get("email", "").lower() == email.lower()]


def updateUsuario(usuario_id: int, data: UsuarioUpdate) -> dict | None:
    rows = _read_all(USUARIOS_CSV, USUARIOS_FIELDS)
    updated = None
    for row in rows[1:]:
        if row["id"] == str(usuario_id):
            changes = {k: v for k, v in data.model_dump().items() if v is not None}
            row.update(changes)
            updated = row
            break
    if updated:
        _write_all(USUARIOS_CSV, USUARIOS_FIELDS, rows)
    return updated


# ─── CRITERIO 5: inactivar en vez de borrar (histórico) ──────────────────
def killUsuario(usuario_id: int) -> dict | None:
    rows = _read_all(USUARIOS_CSV, USUARIOS_FIELDS)
    target = None
    for row in rows[1:]:
        if row["id"] == str(usuario_id):
            row["activo"] = "False"   # soft delete → histórico conservado
            target = row
            break
    if target:
        _write_all(USUARIOS_CSV, USUARIOS_FIELDS, rows)
    return target


# ════════════════════════════════════════════════════════════════════════
#  PRODUCTO
# ════════════════════════════════════════════════════════════════════════

def createProducto(data: ProductoCreate) -> dict:
    rows = _read_all(PRODUCTOS_CSV, PRODUCTOS_FIELDS)
    new_id = _next_id(rows)
    new_row = {"id": new_id, **data.model_dump()}
    with open(PRODUCTOS_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=PRODUCTOS_FIELDS).writerow(new_row)
    return new_row


def findAllProductos(solo_activos: bool = False) -> list[dict]:
    rows = _read_all(PRODUCTOS_CSV, PRODUCTOS_FIELDS)
    data = rows[1:]
    if solo_activos:
        data = [r for r in data if r.get("activo", "True") == "True"]
    return data


def findOneProducto(producto_id: int) -> dict | None:
    for row in findAllProductos():
        if row["id"] == str(producto_id):
            return row
    return None


# ─── CRITERIO 6: filtrar por categoría ───────────────────────────────────
def findProductosByCategoria(categoria: str) -> list[dict]:
    return [r for r in findAllProductos() if r.get("categoria", "").lower() == categoria.lower()]


# ─── CRITERIO 7: búsqueda por nombre (atributo ≠ ID) ─────────────────────
def findProductosByNombre(nombre: str) -> list[dict]:
    return [r for r in findAllProductos() if nombre.lower() in r.get("nombre", "").lower()]


def updateProducto(producto_id: int, data: ProductoUpdate) -> dict | None:
    rows = _read_all(PRODUCTOS_CSV, PRODUCTOS_FIELDS)
    updated = None
    for row in rows[1:]:
        if row["id"] == str(producto_id):
            changes = {k: v for k, v in data.model_dump().items() if v is not None}
            row.update(changes)
            updated = row
            break
    if updated:
        _write_all(PRODUCTOS_CSV, PRODUCTOS_FIELDS, rows)
    return updated


def killProducto(producto_id: int) -> dict | None:
    rows = _read_all(PRODUCTOS_CSV, PRODUCTOS_FIELDS)
    target = None
    for row in rows[1:]:
        if row["id"] == str(producto_id):
            row["activo"] = "False"   # soft delete
            target = row
            break
    if target:
        _write_all(PRODUCTOS_CSV, PRODUCTOS_FIELDS, rows)
    return target


# ════════════════════════════════════════════════════════════════════════
#  PEDIDO PERSONALIZADO
# ════════════════════════════════════════════════════════════════════════

def createPedido(data: PedidoPersonalizadoCreate) -> dict:
    rows = _read_all(PEDIDOS_CSV, PEDIDOS_FIELDS)
    new_id = _next_id(rows)
    new_row = {"id": new_id, **data.model_dump()}
    with open(PEDIDOS_CSV, "a", newline="", encoding="utf-8") as f:
        csv.DictWriter(f, fieldnames=PEDIDOS_FIELDS).writerow(new_row)
    return new_row


def findAllPedidos() -> list[dict]:
    rows = _read_all(PEDIDOS_CSV, PEDIDOS_FIELDS)
    return rows[1:]


def findOnePedido(pedido_id: int) -> dict | None:
    for row in findAllPedidos():
        if row["id"] == str(pedido_id):
            return row
    return None


# ─── CRITERIO 6: filtrar por estado ──────────────────────────────────────
def findPedidosByEstado(estado: str) -> list[dict]:
    return [r for r in findAllPedidos() if r.get("estado", "").lower() == estado.lower()]


# ─── CRITERIO 7: búsqueda por email del usuario ──────────────────────────
def findPedidosByEmail(email: str) -> list[dict]:
    return [r for r in findAllPedidos() if r.get("usuario_email", "").lower() == email.lower()]


def updatePedido(pedido_id: int, data: PedidoPersonalizadoUpdate) -> dict | None:
    rows = _read_all(PEDIDOS_CSV, PEDIDOS_FIELDS)
    updated = None
    for row in rows[1:]:
        if row["id"] == str(pedido_id):
            changes = {k: v for k, v in data.model_dump().items() if v is not None}
            row.update(changes)
            updated = row
            break
    if updated:
        _write_all(PEDIDOS_CSV, PEDIDOS_FIELDS, rows)
    return updated


def killPedido(pedido_id: int) -> dict | None:
    rows = _read_all(PEDIDOS_CSV, PEDIDOS_FIELDS)
    target = None
    for row in rows[1:]:
        if row["id"] == str(pedido_id):
            row["estado"] = "cancelado"   # histórico: no se borra, se cancela
            target = row
            break
    if target:
        _write_all(PEDIDOS_CSV, PEDIDOS_FIELDS, rows)
    return target
