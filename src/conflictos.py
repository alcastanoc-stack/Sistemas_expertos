def resolver_conflicto(reglas_aplicables, hechos_nuevos):
    """Resolución de conflictos por capas, sobre tuplas (índice, regla) como en clase.

    La refracción (a) la aplica el motor con 'reglas_disparadas'.
    Capas, en orden:
      0) prioridad explícita (saliencia, como CLIPS)            [nuevo]
      b) mayor número de antecedentes (especificidad)           [de clase]
      c) antecedentes recién agregados (recencia, como OPS5)    [comentado en clase]
      d) desempate determinista por orden de definición         [en clase era "al azar"]
    Devuelve ((índice, regla), criterio_usado).
    """
    candidatas = list(reglas_aplicables)
    if len(candidatas) == 1:
        return candidatas[0], "única regla aplicable"

    capas = [
        ("prioridad", lambda item: item[1].get("prioridad", 0)),
        ("especificidad", lambda item: len(item[1]["antecedentes"])),
        ("recencia", lambda item: len(set(item[1]["antecedentes"]) & hechos_nuevos)),
    ]
    for nombre, clave in capas:
        mejor = max(clave(item) for item in candidatas)
        candidatas = [item for item in candidatas if clave(item) == mejor]
        if len(candidatas) == 1:
            return candidatas[0], nombre

    # d) empate total: se toma la primera en el orden del archivo
    return candidatas[0], "orden de definición"