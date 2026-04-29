import csv
import os

USUARIOS_CSV  = "usuarios.csv"
PRODUCTOS_CSV = "productos.csv"
PEDIDOS_CSV   = "pedidos_personalizados.csv"

USUARIOS_FIELDS  = ["id", "nombre_real", "email", "direccion_envio", "contrasena", "activo"]
PRODUCTOS_FIELDS = ["id", "nombre", "descripcion", "precio", "categoria", "stock", "activo"]
PEDIDOS_FIELDS   = ["id", "usuario_email", "producto_id", "descripcion",
                    "talla", "color", "precio_estimado", "estado"]


def _init_csv(filepath: str, fields: list[str]) -> None:
    if not os.path.exists(filepath):
        with open(filepath, "w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=fields)
            writer.writeheader()


def init_all_csv() -> None:
    _init_csv(USUARIOS_CSV,  USUARIOS_FIELDS)
    _init_csv(PRODUCTOS_CSV, PRODUCTOS_FIELDS)
    _init_csv(PEDIDOS_CSV,   PEDIDOS_FIELDS)
