from src.cargador import cargar_reglas, cargar_hechos
from src.motor import MotorPasoAPaso, motor_inferencia_avanzado

_, REGLAS = cargar_reglas("conocimiento/red.json")


def correr(caso):
    m = MotorPasoAPaso(cargar_hechos(f"ejemplos/{caso}.json"), REGLAS)
    m.ejecutar()
    return m


def test_dns_encadena_tres_niveles():
    m = correr("caso_01_dns")
    assert {"falla_dns", "dns_local_incorrecto", "recomendar_cambiar_dns"} <= set(m.memoria)


def test_dhcp():
    assert "recomendar_reiniciar_router" in correr("caso_02_dhcp").memoria


def test_conflicto_gana_prioridad():
    m = correr("caso_03_conflicto")
    assert m.historial[0]["regla"].startswith("R02")
    assert m.historial[0]["criterio"] == "prioridad"


def test_hecho_falso_se_ignora():
    assert "router_sin_luces" not in correr("caso_03_conflicto").memoria


def test_funcion_de_clase_en_consola():
    hechos = motor_inferencia_avanzado(cargar_hechos("ejemplos/caso_01_dns.json"), REGLAS)
    assert "recomendar_cambiar_dns" in hechos


def test_hay_15_reglas_o_mas():
    assert len(REGLAS) >= 15