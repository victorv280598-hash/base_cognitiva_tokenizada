"""
==============================================================================
PROYECTO: Sistema Cognitivo LLM - Núcleo Aislado de Mínima Acción
REPOSITORIO: https://github.com/victorv280598-hash/base_cognitiva_tokenizada
ARCHIVO: prueba_sistema.py
AUTOR: Victor Jose Vazquez Preciado
LICENCIA: Todos los derechos reservados (All Rights Reserved).
DESCRIPCIÓN: Suite de pruebas automatizadas en Python puro (cero dependencias)
para verificar la descarga desde GitHub, la tokenización aislada y el cálculo
de Entropía y Mínima Acción (δS = 0).
==============================================================================
"""

import urllib.request
import json
import re
import cmath
import time

# ==============================================================================
# 1. PARÁMETROS AJUSTABLES DE LA PRUEBA
# ==============================================================================
URL_BASE_GITHUB = "https://raw.githubusercontent.com/victorv280598-hash/base_cognitiva_tokenizada/main/base_cognitiva_tokenizada.json"
UMBRAL_ENTROPIA = 0.65
H_BARRA_COMPUTACIONAL = 1.0
PATRON_TOKENS = r'[\w-]+|[#$&\[\]]'

# Casos de prueba predefinidos para validar todas las rutas de tu arquitectura
CASOS_DE_PRUEBA = [
    "Explícame la ley De Morgan 1",
    "¿Qué hace el símbolo $ de anclaje?",
    "Dame la estructura RTCFR",
    "Consulta sobre física cuántica avanzada no registrada"
]


# ==============================================================================
# 2. FUNCIONES DEL MOTOR DE EVALUACIÓN
# ==============================================================================
def descargar_base(url: str) -> dict:
    """Descarga y valida la estructura JSON desde GitHub."""
    with urllib.request.urlopen(url, timeout=10) as respuesta:
        datos = json.loads(respuesta.read().decode("utf-8"))
        return datos


def evaluar_consulta(consulta: str, conceptos: dict) -> dict:
    """Aplica intersección A ∩ B y calcula Entropía y Acción S."""
    tokens_usuario = set(re.findall(PATRON_TOKENS, consulta.lower()))
    if not tokens_usuario:
        return {"estado": "INHIBIDO", "mensaje": "Entrada vacía."}

    candidatos = []
    for id_concepto, info in conceptos.items():
        tokens_concepto = set(info["metricas_tokens"]["tokens_unicos"])
        coincidencias = tokens_usuario.intersection(tokens_concepto)

        if coincidencias:
            relevancia = len(coincidencias) / len(tokens_usuario)
            entropia = round(1.0 - relevancia, 4)
            costo_tokens = info["metricas_tokens"]["cantidad_total"]
            accion_s = round(costo_tokens * (1.0 + entropia), 4)
            fase = cmath.exp(1j * (accion_s / H_BARRA_COMPUTACIONAL))

            candidatos.append({
                "id": id_concepto,
                "nombre": info["nombre"],
                "sintaxis": info["sintaxis"],
                "entropia": entropia,
                "accion_s": accion_s,
                "fase_real": round(fase.real, 4)
            })

    if not candidatos:
        return {
            "estado": "DETENIDO_AHORRO",
            "mensaje": "Sin coincidencias en memoria aislada (Cero gasto adicional)."
        }

    # Ordenamos por menor Acción S (Principio de Mínima Acción: δS -> 0)
    candidatos.sort(key=lambda x: x["accion_s"])
    ganador = candidatos[0]
    ganador["estado"] = "SISTEMA_1_OPTIMO" if ganador["entropia"] <= UMBRAL_ENTROPIA else "SISTEMA_1_BAJA_COINCIDENCIA"
    return ganador


# ==============================================================================
# 3. EJECUCIÓN DE LA BATERÍA DE PRUEBAS
# ==============================================================================
def ejecutar_diagnostico():
    print("=================================================================")
    print("🧪 INICIANDO PRUEBA DEL SISTEMA COGNITIVO DE MÍNIMA ACCIÓN")
    print("=================================================================")

    inicio = time.perf_counter()
    try:
        base = descargar_base(URL_BASE_GITHUB)
    except Exception as error:
        print(f"❌ FALLO DE CONEXIÓN: No se pudo leer el archivo JSON en GitHub.")
        print(f"   Detalle técnico: {error}")
        print("   Asegúrate de que 'base_cognitiva_tokenizada.json' exista en 'main'.")
        return

    conceptos = base.get("conceptos_aislados", {})
    tiempo_carga = round((time.perf_counter() - inicio) * 1000, 2)

    print(f"✅ Conexión exitosa en {tiempo_carga} ms")
    print(f"📦 Conceptos aislados verificados: {len(conceptos)}")
    print("-----------------------------------------------------------------\n")

    for indice, pregunta in enumerate(CASOS_DE_PRUEBA, start=1):
        t0 = time.perf_counter()
        resultado = evaluar_consulta(pregunta, conceptos)
        duracion_ms = round((time.perf_counter() - t0) * 1000, 4)

        print(f"Prueba #{indice}: '{pregunta}'")
        print(f"  ⏱️ Tiempo CPU : {duracion_ms} ms")
        print(f"  📌 Ruta/Estado: {resultado['estado']}")

        if "id" in resultado:
            print(f"  🆔 Match      : [{resultado['id']}] {resultado['nombre']}")
            print(f"  ⚡ Métricas   : Entropía = {resultado['entropia']} | Acción S = {resultado['accion_s']} | Fase = {resultado['fase_real']}")
            print(f"  🧩 Sintaxis   : {resultado['sintaxis']}\n")
        else:
            print(f"  ℹ️ Aviso      : {resultado['mensaje']}\n")

    print("=================================================================")
    print("🏁 DIAGNÓSTICO COMPLETADO CON ÉXITO")
    print("=================================================================")


if __name__ == "__main__":
    ejecutar_diagnostico()
