import re
from fastapi import HTTPException

def extraer_campo_foreign_key(error_msg: str) -> str:
    match = re.search(r'la llave \((\w+)\)=', error_msg)
    if match:
        return match.group(1)

    match = re.search(r'Key \((\w+)\)=', error_msg)
    if match:
        return match.group(1)

    match = re.search(r'viola la llave foránea «([\w_]+)_fkey»', error_msg)
    if not match:
        match = re.search(r'violates foreign key constraint "([\w_]+)_fkey"', error_msg)

    if match:
        partes = match.group(1).split("_")
        for i, parte in enumerate(partes):
            if parte == "cod":
                return "_".join(partes[i:])
        return partes[-1]

    return "campo_desconocido"

def extraer_campo_null(error_msg: str) -> str:
    match = re.search(r'null value in column "(\w+)"', error_msg)
    return match.group(1) if match else "campo_desconocido"

def validar_tipo_modelo(tipo_modelo: str) -> None:
    """
    Verifica que el tipo_modelo tenga un formato válido de identificador SQL.
    Solo permite letras, números y guiones bajos, y que no empiece con un número.
    """
    if not re.match(r"^[a-zA-Z_][a-zA-Z0-9_]*$", tipo_modelo):
        raise HTTPException(
            status_code=400,
            detail="El tipo_modelo contiene caracteres inválidos."
        )