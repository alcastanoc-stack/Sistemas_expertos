import json


def _leer(fuente):
    if hasattr(fuente, "read"):             # archivo subido en la interfaz
        if hasattr(fuente, "seek"):
            fuente.seek(0)
        return json.load(fuente)
    with open(fuente, encoding="utf-8") as f:
        return json.load(f)


def cargar_reglas(fuente):
    """Lee el JSON y devuelve (dominio, lista de reglas) con la misma estructura
    de diccionarios del código de clase. El texto de 'accion' se convierte en una
    función callable, como las lambda del original."""
    datos = _leer(fuente)
    if "reglas" not in datos:
        raise ValueError("El archivo no tiene la clave 'reglas'.")
    reglas, nombres = [], set()
    for i, r in enumerate(datos["reglas"]):
        for campo in ("nombre", "antecedentes", "consecuentes"):
            if campo not in r:
                raise ValueError(f"Regla #{i + 1}: falta el campo '{campo}'.")
        if r["nombre"] in nombres:
            raise ValueError(f"Nombre de regla repetido: {r['nombre']}")
        nombres.add(r["nombre"])
        regla = {
            "nombre": r["nombre"],
            "antecedentes": r["antecedentes"],
            "consecuentes": r["consecuentes"],
            "prioridad": r.get("prioridad", 0),
            "explicacion": r.get("explicacion", ""),
            "accion_texto": r.get("accion", ""),
        }
        if regla["accion_texto"]:
            regla["accion"] = (lambda hechos_actuales, t=regla["accion_texto"]:
                               print(f"¡Recomendación: {t}"))
        reglas.append(regla)
    return datos.get("dominio", ""), reglas


def cargar_hechos(fuente):
    """Devuelve un diccionario {hecho: bool}, como los datos_paciente de clase.
    Acepta {"hechos": {"x": true}} o {"hechos": ["x"]}."""
    datos = _leer(fuente)
    if "hechos" not in datos:
        raise ValueError("El archivo no tiene la clave 'hechos'.")
    h = datos["hechos"]
    if isinstance(h, dict):
        return dict(h)
    return {x: True for x in h}