# Sistema Experto: 

Sistema experto basado en reglas con **encadenamiento hacia adelante** que diagnostica fallas de conectividad de red a partir de síntomas y entrega una recomendación. Cuenta con base de conocimiento externa (JSON), estrategia de resolución de conflictos por capas e interfaz web que muestra la inferencia paso a paso.

## Integrantes

- ALEXANDRA CASTAÑO CELIS–  acastanoc@unal.edu.co
- SEBASTIAN NARANJO BERNAL– senaranjob@unal.edu.co

## Requisitos

- Python 3.10 o superior
- GitHub para clonar el repositorio

## Instalación

```bash
git clone https://github.com/alcastanoc-stack/Sistemas_expertos.git
cd Sistemas_expertos
python -m venv venv
venv\Scripts\activate          # Windows
# source venv/bin/activate     # Mac/Linux
pip install -r requirements.txt
```

## Dependencias

| Paquete   | Versión | Uso                         |
|-----------|---------|-----------------------------|
| streamlit | >=1.30  | Interfaz web                |

El resto del sistema usa solo la librería estándar de Python (`json`, `dataclasses`).

## Ejecución

```bash
py -m streamlit run src/app.py
```

En la interfaz:

1. Cargar la base de conocimiento (`conocimiento/red.json`).
2. Cargar un caso de `ejemplos/` o marcar los síntomas manualmente.
3. Pulsar **Siguiente paso** para ver cada regla disparada, el conjunto conflicto, el criterio de desempate y la memoria de trabajo.
4. Revisar la recomendación final.

## Estructura de carpetas

```
Sistemas_expertos/
├── README.md
├── base_codi_clase/
│   └── motor_originalProf.py  //código original entregado en clase (sin modificar)
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── motor.py          # ciclo de inferencia: emparejar → resolver conflicto → disparar
│   ├── conflictos.py     # estrategia de resolución de conflictos
│   ├── cargador.py       # lectura y validación de los archivos JSON
│   └── app.py            # interfaz Streamlit
├── conocimiento/
│   └── red.json          # base de conocimiento (17 reglas con encadenamiento)
├── ejemplos/
│   ├── caso_01_dns.json
│   ├── caso_02_dhcp.json
│   └── caso_03_conflicto.json
├── docs/
│   └── documento_tecnico.pdf
└── tests/
    └── test_motor.py
```

- `src/`: código fuente del sistema.
- `conocimiento/`: base de conocimiento externa.
- `ejemplos/`: casos de hechos iniciales para probar el sistema.
- `docs/`: documento técnico (arquitectura, hechos, conflictos, decisiones y uso de IA).
- `tests/`: pruebas del motor.

## Formato de la base de conocimiento

```json
{
  "dominio": "Diagnóstico de conectividad de red",
  "reglas": [
    {
      "nombre": "R06 Falla DNS",
      "antecedentes": ["ping_ip_publica_ok", "ping_dominio_falla"],
      "consecuentes": ["falla_dns"],
      "prioridad": 6,
      "explicacion": "Hay salida a internet por IP pero no resuelve nombres."
    }
  ]
}
```

## Formato de los hechos iniciales

```json
{
  "hechos": {"ping_gateway_ok": true, "ping_ip_publica_ok": true, "ping_dominio_falla": true, "otros_dispositivos_ok": true}
}
```

## Estrategia de resolución de conflictos

Cuando varias reglas pueden ejecutarse al mismo tiempo, el sistema utiliza los siguientes criterios para elegir cuál aplicar:

1. **No repetición: evita ejecutar nuevamente una regla que ya se disparó durante la sesión.

2. **Prioridad: selecciona la regla con el valor de prioridad más alto.

3. **Especificidad: si hay empate, favorece la regla que tenga más antecedentes.

4. **Recencia: si continúa el empate, favorece la regla que tenga más antecedentes entre los hechos agregados por la última regla ejecutada.

5. **Orden de definición: si persiste el empate, selecciona la primera regla según su posición en el archivo JSON.

La estrategia toma como referencia criterios de resolución de conflictos asociados con Bigus, Rolston, CLIPS y OPS5. La prioridad y el desempate por orden de definición son adaptaciones realizadas para este proyecto. Para más detalles, consultar el documento técnico.

## Casos de ejemplo

| Archivo | Qué demuestra |
|---------|---------------|
| `caso_01_dns.json` | Encadenamiento de 3 niveles hasta recomendar cambiar el DNS |
| `caso_02_dhcp.json` | Diagnóstico de falla de DHCP y recomendación sobre el router |
| `caso_03_conflicto.json` | Dos reglas compiten y se resuelve por la estrategia de conflictos |

## Documento técnico

Ver [docs/documento_tecnico.pdf](docs/documento_tecnico.pdf). Incluye la declaración de uso de herramientas de IA generativa.