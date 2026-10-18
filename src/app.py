import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

import streamlit as st
from src.cargador import cargar_reglas, cargar_hechos
from src.motor import MotorPasoAPaso

RAIZ = Path(__file__).resolve().parent.parent

st.set_page_config(page_title="Sistema Experto de Redes", layout="wide")
st.title("Sistema experto: diagnóstico de conectividad de red")

st.sidebar.header("1. Base de conocimiento")
kb_file = st.sidebar.file_uploader("Archivo JSON de reglas", type="json")
try:
    dominio, reglas = cargar_reglas(kb_file or RAIZ / "conocimiento" / "red.json")
except Exception as e:
    st.error(f"Error en la base de conocimiento: {e}")
    st.stop()
st.sidebar.caption(f"{dominio}: {len(reglas)} reglas")

st.sidebar.header("2. Hechos iniciales")
hechos_file = st.sidebar.file_uploader("Archivo JSON de hechos", type="json")
consecuentes = {c for r in reglas for c in r["consecuentes"]}
observables = sorted({a for r in reglas for a in r["antecedentes"]} - consecuentes)
defecto = []
if hechos_file:
    try:
        defecto = [h for h, v in cargar_hechos(hechos_file).items() if v and h in observables]
    except Exception as e:
        st.sidebar.error(str(e))
hechos = st.sidebar.multiselect(
    "O marca los síntomas manualmente", observables, default=defecto,
    key=f"hechos_{hechos_file.name if hechos_file else 'manual'}")

if st.sidebar.button("Iniciar / Reiniciar", type="primary"):
    st.session_state.motor = MotorPasoAPaso({h: True for h in hechos}, reglas)

motor = st.session_state.get("motor")
if motor is None:
    st.info("Carga la base y los hechos, y pulsa **Iniciar / Reiniciar**.")
    st.stop()

c1, c2 = st.columns(2)
if c1.button("Siguiente paso"):
    if motor.paso() is None:
        st.toast("No hay más reglas aplicables.")
if c2.button("Ejecutar todo"):
    motor.ejecutar()

izq, der = st.columns([2, 1])
with izq:
    st.subheader("Inferencia paso a paso")
    if not motor.historial:
        st.write("Aún no se ha disparado ninguna regla.")
    for p in motor.historial:
        with st.expander(f"Paso {p['paso']}: {p['regla']}", expanded=True):
            st.write(f"**Conjunto conflicto:** {', '.join(p['conjunto_conflicto'])}")
            st.write(f"**Regla elegida:** {p['regla']} — criterio: *{p['criterio']}*")
            st.write(f"**Antecedentes:** {', '.join(p['antecedentes'])}")
            st.write(f"**Hechos nuevos:** {', '.join(p['hechos_nuevos']) or 'ninguno'}")
            if p["accion"]:
                st.write(f"**Acción:** {p['accion']}")
            st.caption(p["explicacion"])
with der:
    st.subheader("Memoria de trabajo")
    for h in motor.memoria:
        st.code(h)

st.subheader("Recomendación")
if not motor.terminado:
    st.warning("La inferencia aún no termina. Sigue con **Siguiente paso**.")
elif motor.recomendaciones():
    for rec in motor.recomendaciones():
        st.success(rec)
else:
    st.error("Con los hechos dados no se llegó a ninguna recomendación.")