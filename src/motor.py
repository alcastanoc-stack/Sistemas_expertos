from src.conflictos import resolver_conflicto


def motor_paso_a_paso(datos_iniciales, reglas):
    """Mismo algoritmo de motor_inferencia_avanzado (código de clase), pero como
    generador: entrega un registro por cada regla disparada, para la interfaz."""
    memoria = [h for h, valor in datos_iniciales.items() if valor]  # solo hechos verdaderos
    hechos = set(memoria)          # Convertir datos iniciales a hechos
    hechos_nuevos = set()          # Hechos recién agregados por la última regla disparada
    reglas_disparadas = set()
    paso = 0

    while True:
        reglas_aplicables = []
        for i, regla in enumerate(reglas):
            # a) No repetir reglas ya disparadas
            if i not in reglas_disparadas:
                antecedentes = set(regla["antecedentes"])
                # Aplica si todos los antecedentes están en los hechos actuales
                if antecedentes.issubset(hechos):
                    reglas_aplicables.append((i, regla))

        if not reglas_aplicables:
            break  # No hay reglas aplicables, detener la inferencia

        # *****  Resolver conflicto (ver conflictos.py)  *****
        (indice_regla_seleccionada, regla_seleccionada), criterio = resolver_conflicto(
            reglas_aplicables, hechos_nuevos)

        # Disparar la regla y agregar nuevos hechos (consecuentes)
        reglas_disparadas.add(indice_regla_seleccionada)
        hechos_nuevos = set()
        nuevos_hechos_inferidos_por_regla = []
        for consecuente in regla_seleccionada["consecuentes"]:
            if consecuente not in hechos:
                hechos_nuevos.add(consecuente)
                hechos.add(consecuente)
                memoria.append(consecuente)
                nuevos_hechos_inferidos_por_regla.append(consecuente)

        # Ejecutar acción si existe (opcional)
        if "accion" in regla_seleccionada and callable(regla_seleccionada["accion"]):
            regla_seleccionada["accion"](hechos)

        paso += 1
        yield {
            "paso": paso,
            "conjunto_conflicto": [r["nombre"] for _, r in reglas_aplicables],
            "regla": regla_seleccionada["nombre"],
            "criterio": criterio,
            "explicacion": regla_seleccionada.get("explicacion", ""),
            "antecedentes": regla_seleccionada["antecedentes"],
            "hechos_nuevos": nuevos_hechos_inferidos_por_regla,
            "accion": regla_seleccionada.get("accion_texto", ""),
            "memoria": list(memoria),
        }


def motor_inferencia_avanzado(datos_iniciales, reglas):
    """Versión de consola, con los mismos print del código de clase."""
    hechos = [h for h, valor in datos_iniciales.items() if valor]
    for p in motor_paso_a_paso(datos_iniciales, reglas):
        print("\nConjunto de conflictos (Reglas aplicables):")
        for nombre in p["conjunto_conflicto"]:
            print(f"- {nombre}")
        print(f"\nRegla seleccionada: {p['regla']} (criterio: {p['criterio']})")
        if p["hechos_nuevos"]:
            print(f"Regla disparada: {p['regla']}. Nuevos hechos agregados: {', '.join(p['hechos_nuevos'])}")
        else:
            print(f"Regla disparada: {p['regla']}. No se agregaron nuevos hechos.")
        hechos = p["memoria"]
    print("\nConjunto de conflictos (Reglas aplicables):")
    print("- Ninguna")
    return hechos


class MotorPasoAPaso:
    """Envuelve el generador para avanzar una regla por vez desde la interfaz."""

    def __init__(self, datos_iniciales, reglas):
        self.reglas = reglas
        self.inicial = [h for h, valor in datos_iniciales.items() if valor]
        self.historial = []
        self._gen = motor_paso_a_paso(datos_iniciales, reglas)
        self._siguiente = next(self._gen, None)   # mira un paso adelante

    @property
    def terminado(self):
        return self._siguiente is None

    @property
    def memoria(self):
        return self.historial[-1]["memoria"] if self.historial else self.inicial

    def paso(self):
        if self._siguiente is None:
            return None
        registro = self._siguiente
        self._siguiente = next(self._gen, None)
        self.historial.append(registro)
        return registro

    def ejecutar(self):
        while self.paso():
            pass

    def recomendaciones(self):
        return [p["accion"] for p in self.historial if p["accion"]]


if __name__ == "__main__":
    # Ejecución por consola, como en el código de clase:  py -m src.motor
    from src.cargador import cargar_reglas, cargar_hechos
    _, reglas_red = cargar_reglas("conocimiento/red.json")
    for caso in ("caso_01_dns", "caso_02_dhcp", "caso_03_conflicto"):
        print(f"\n--- Ejecutando motor de inferencia para {caso} ---")
        inferidos = motor_inferencia_avanzado(cargar_hechos(f"ejemplos/{caso}.json"), reglas_red)
        print(f"\nHechos inferidos para {caso}:", inferidos)