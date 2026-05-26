"""routers/pedidos.py — CRUD de pedidos personalizados."""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select

from db import get_session
from models import PedidoPersonalizado, PedidoCreate, PedidoUpdate
from auth import get_current_user, require_admin, Usuario

router = APIRouter(prefix="/pedido", tags=["Pedido"])


@router.post("/", response_model=PedidoPersonalizado, status_code=201)
def create_pedido(
    data: PedidoCreate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    pedido = PedidoPersonalizado(**data.model_dump())
    pedido.usuario_email = current_user.email
    session.add(pedido)
    session.commit()
    session.refresh(pedido)
    return pedido


@router.get("/mis-pedidos", response_model=List[PedidoPersonalizado])
def mis_pedidos(
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    return session.exec(
        select(PedidoPersonalizado).where(PedidoPersonalizado.usuario_email == current_user.email)
    ).all()


@router.get("/", response_model=List[PedidoPersonalizado])
def list_pedidos(
    estado: Optional[str] = Query(None),
    session: Session = Depends(get_session),
    _: Usuario = Depends(require_admin),
):
    q = select(PedidoPersonalizado)
    if estado:
        q = q.where(PedidoPersonalizado.estado == estado)
    return session.exec(q).all()


@router.patch("/{pedido_id}", response_model=PedidoPersonalizado)
def update_pedido(
    pedido_id: int,
    data: PedidoUpdate,
    session: Session = Depends(get_session),
    _: Usuario = Depends(require_admin),
):
    p = session.get(PedidoPersonalizado, pedido_id)
    if not p:
        raise HTTPException(404, "Pedido no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    session.commit()
    session.refresh(p)
    return p


@router.delete("/{pedido_id}")
def cancel_pedido(
    pedido_id: int,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    p = session.get(PedidoPersonalizado, pedido_id)
    if not p:
        raise HTTPException(404, "Pedido no encontrado")
    if p.usuario_email != current_user.email and current_user.rol != "admin":
        raise HTTPException(403, "No autorizado")
    p.estado = "cancelado"
    session.commit()
    return {"mensaje": "Pedido cancelado"}