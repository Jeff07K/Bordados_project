from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from db import get_session
from models import Producto, ProductoCreate, ProductoUpdate, Usuario
from auth import get_current_user, require_admin

router = APIRouter(prefix="/producto", tags=["Producto"])

@router.get("/", response_model=List[Producto])
def list_productos(
    solo_activos: bool = Query(True),
    categoria: Optional[str] = Query(None),
    session: Session = Depends(get_session),
):
    q = select(Producto)
    if solo_activos:
        q = q.where(Producto.activo == True)
    if categoria:
        q = q.where(Producto.categoria == categoria)
    return session.exec(q).all()

@router.get("/{producto_id}", response_model=Producto)
def get_producto(producto_id: int, session: Session = Depends(get_session)):
    p = session.get(Producto, producto_id)
    if not p:
        raise HTTPException(404, "Producto no encontrado")
    return p

@router.post("/", response_model=Producto, status_code=201)
def create_producto(
    data: ProductoCreate,
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    p = Producto(**data.model_dump())
    session.add(p)
    session.commit()
    session.refresh(p)
    return p

@router.patch("/{producto_id}", response_model=Producto)
def update_producto(
    producto_id: int,
    data: ProductoUpdate,
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    p = session.get(Producto, producto_id)
    if not p:
        raise HTTPException(404, "Producto no encontrado")
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(p, k, v)
    session.commit()
    session.refresh(p)
    return p

@router.delete("/{producto_id}")
def delete_producto(
    producto_id: int,
    session: Session = Depends(get_session),
    _: dict = Depends(require_admin),
):
    p = session.get(Producto, producto_id)
    if not p:
        raise HTTPException(404, "Producto no encontrado")
    p.activo = False
    session.commit()
    return {"mensaje": "Producto desactivado (histórico conservado)"}