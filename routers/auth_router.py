from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session, select
from db import get_session
from models import Usuario, UsuarioCreate, UsuarioPublic
from auth import get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Autenticación"])

@router.post("/register", response_model=UsuarioPublic, status_code=201)
def register(data: UsuarioCreate, session: Session = Depends(get_session)):
    existe = session.exec(select(Usuario).where(Usuario.email == data.email)).first()
    if existe:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    usuario = Usuario(
        nombre_real=data.nombre_real,
        email=data.email,
        direccion_envio=data.direccion_envio,
        contrasena_hash=get_password_hash(data.contrasena),
    )
    session.add(usuario)
    session.commit()
    session.refresh(usuario)
    return usuario

@router.post("/login")
def login(
    form: OAuth2PasswordRequestForm = Depends(),
    session: Session = Depends(get_session),
):
    usuario = session.exec(select(Usuario).where(Usuario.email == form.username)).first()
    if not usuario or not verify_password(form.password, usuario.contrasena_hash):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    if not usuario.activo:
        raise HTTPException(status_code=403, detail="Cuenta desactivada")
    token = create_access_token({"sub": usuario.email, "rol": usuario.rol})
    return {
        "access_token": token,
        "token_type": "bearer",
        "rol": usuario.rol,
        "nombre": usuario.nombre_real,
    }