"""routers/usuarios.py — Gestión de usuarios (admin)."""
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select

from db import get_session
from models import Usuario, UsuarioPublic, UsuarioUpdate
from auth import get_current_user, require_admin

router = APIRouter(prefix="/usuario", tags=["Usuario"])


@router.get("/me", response_model=UsuarioPublic)
def get_me(current_user: Usuario = Depends(get_current_user)):
    return current_user


@router.patch("/me", response_model=UsuarioPublic)
def update_me(
    data: UsuarioUpdate,
    session: Session = Depends(get_session),
    current_user: Usuario = Depends(get_current_user),
):
    for k, v in data.model_dump(exclude_unset=True).items():
        setattr(current_user, k, v)
    session.add(current_user)
    session.commit()
    session.refresh(current_user)
    return current_user


@router.get("/", response_model=List[UsuarioPublic])
def list_usuarios(
    session: Session = Depends(get_session),
    _: Usuario = Depends(require_admin),
):
    return session.exec(select(Usuario)).all()


@router.delete("/{usuario_id}")
def deactivate_usuario(
    usuario_id: int,
    session: Session = Depends(get_session),
    _: Usuario = Depends(require_admin),
):
    u = session.get(Usuario, usuario_id)
    if not u:
        raise HTTPException(404, "Usuario no encontrado")
    u.activo = False
    session.commit()
    return {"mensaje": "Usuario desactivado"}