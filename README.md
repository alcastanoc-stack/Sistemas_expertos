# Sistema Experto: 

Sistema experto basado en reglas con **encadenamiento hacia adelante** que diagnostica fallas de conectividad de red a partir de síntomas y entrega una recomendación. Cuenta con base de conocimiento externa (JSON), estrategia de resolución de conflictos por capas e interfaz web que muestra la inferencia paso a paso.

## Integrantes

- ALEXANDRA CASTAÑO CELIS–  acastanoc@unal.edu.co
- SEBASTIAN NARANJO BERNAL– senaranjob@unal.edu.co

## Requisitos

- Python 3.10 o superior
- GitHub

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
streamlit run src/app.py
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
├── requirements.txt
├── .gitignore
├── src/
│   ├── __init__.py
│   ├── motor.py          # ciclo de inferencia: emparejar → resolver conflicto → disparar
│   ├── conflictos.py     # estrategia de resolución de conflictos
│   ├── cargador.py       # lectura y validación de los archivos JSON
│   └── app.py            # interfaz Streamlit
├── conocimiento/
│   └── red.json          # base de conocimiento (16 reglas con encadenamiento)
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
      "id": "R06",
      "si": ["ping_ip_publica_ok", "ping_dominio_falla"],
      "entonces": ["falla_dns"],
      "prioridad": 5,
      "explicacion": "Hay salida a internet por IP pero no resuelve nombres."
    }
  ]
}
```

## Formato de los hechos iniciales

```json
{
  "hechos": ["ping_gateway_ok", "ping_ip_publica_ok", "ping_dominio_falla"]
}
```

## Estrategia de resolución de conflictos

Se aplica en este orden: refracción, prioridad explícita (saliencia), especificidad, recencia y orden de definición. Referentes: OPS5 (Forgy), CLIPS y Giarratano & Riley. El detalle está en el documento técnico.

## Casos de ejemplo

| Archivo | Qué demuestra |
|---------|---------------|
| `caso_01_dns.json` | Encadenamiento de 3 niveles hasta recomendar cambiar el DNS |
| `caso_02_dhcp.json` | Diagnóstico de falla de DHCP y recomendación sobre el router |
| `caso_03_conflicto.json` | Dos reglas compiten y se resuelve por la estrategia de conflictos |

## Documento técnico

Ver [docs/documento_tecnico.pdf](docs/documento_tecnico.pdf). Incluye la declaración de uso de herramientas de IA generativa.