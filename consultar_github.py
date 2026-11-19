"""
==============================================================================
PROYECTO: Sistema Cognitivo LLM - Núcleo Aislado de Mínima Acción
ARCHIVO: consultar_github.py
AUTOR: Victor Jose Vazquez Preciado
LICENCIA: Todos los derechos reservados (All Rights Reserved).
DESCRIPCIÓN: Motor determinista de consulta ligera que lee la base aislada
desde GitHub y aplica el Principio de Mínima Acción (δS = 0) con gasto
computacional cercano a cero (sin inferencia de modelos externos).
==============================================================================
"""

import urllib.request
import json
import re
import cmath

# ==============================================================================
# 1. PARÁMETROS AJUSTABLES DEL SISTEMA
# ==============================================================================
# Ruta directa (Raw) a tu base de conceptos aislados en GitHub
URL_BASE_GITHUB = "https://raw.githubusercontent.com/victorv280598-hash/sistema-cognitivo-aislado/main/base_cognitiva_tokenizada.json"

# Umbrales metacognitivos extraídos de tu arquitectura
UMBRAL_ENTROPIA = 0.65        # Si la duda supera este valor, se marca baja coincidencia
H_BARRA_COMPUTACIONAL = 1.0   # Constante de escala para el cálculo de fase compleja
PATRON_TOKENS = r'[\w-]+|[#$&\[\]]'  # Conserva palabras y tus símbolos (#, $, &, [, ])


# ==============================================================================
# 2. FUNCIONES DE CONEXIÓN Y TOKENIZACIÓN LIGERA
# ==============================================================================
def cargar_base_desde_github(url: str) -> dict:
    """
    Descarga el archivo JSON de conceptos aislados desde GitHub usando
    únicamente librerías estándar de Python (sin consumo de dependencias).
    """
    try:
        with urllib.request.urlopen(url, timeout=10) as respuesta:
            contenido_texto = respuesta.read().decode("utf-8")
            return json.loads(contenido_texto)
    except Exception as error:
        print(f"⚠️ Error de conexión con GitHub: {error}")
        print("Verifica que el repositorio 'sistema-cognitivo-aislado' sea público")
        print("y que el archivo 'base_cognitiva_tokenizada.json' exista en 'main'.")
        return {}


def tokenizar_consulta(texto: str) -> set[str]:
    """
    Convierte la pregunta del usuario en un conjunto de tokens únicos en minúsculas.
    Operación O(n) de costo computacional prácticamente nulo.
    """
    lista_tokens = re.findall(PATRON_TOKENS, texto.lower())
    return set(lista_tokens)


# ==============================================================================
# 3. NÚCLEO DE EVALUACIÓN DE ENTROPÍA Y MÍNIMA ACCIÓN (δS = 0)
# ==============================================================================
def buscar_y_evaluar_accion(consulta: str, base_datos: dict) -> dict:
    """
    Ejecuta el flujo cognitivo determinista:
    1. Control Inhibitorio: Filtra consultas vacías.
    2. Intersección (A ∩ B): Cruza tokens de consulta contra tokens aislados.
    3. Principio de Mínima Acción: Calcula Acción S = Costo * (1 + Entropía) y elige
       la ruta con menor consumo energético (δS -> 0).
    """
    conceptos = base_datos.get("conceptos_aislados", {})
    if not conceptos:
        return {"estado": "ERROR", "mensaje": "No se encontraron conceptos en el JSON."}

    # Paso 1: Control Inhibitorio de entrada
    tokens_usuario = tokenizar_consulta(consulta)
    if not tokens_usuario:
        return {"estado": "INHIBIDO", "mensaje": "Entrada vacía. Ejecución detenida."}

    candidatos = []

    # Paso 2: Intersección de conjuntos (A ∩ B)
    for id_concepto, info in conceptos.items():
        tokens_concepto = set(info["metricas_tokens"]["tokens_unicos"])
        coincidencias = tokens_usuario.intersection(tokens_concepto)

        if coincidencias:
            # Cálculo de certeza y entropía (incertidumbre)
            relevancia = len(coincidencias) / len(tokens_usuario)
            entropia = round(1.0 - relevancia, 4)
            costo_tokens = info["metricas_tokens"]["cantidad_total"]

            # Cálculo de Acción S y amplitud de fase e^(i/ħ * S)
            accion_s = round(costo_tokens * (1.0 + entropia), 4)
            fase = cmath.exp(1j * (accion_s / H_BARRA_COMPUTACIONAL))

            candidatos.append({
                "id": id_concepto,
                "nombre": info["nombre"],
                "tipo": info["tipo"],
                "sintaxis": info["sintaxis"],
                "detalle": info["detalle"],
                "entropia": entropia,
                "accion_s": accion_s,
                "fase_real": round(fase.real, 4),
                "fase_imaginaria": round(fase.imag, 4)
            })

    # Si no hay intersección, detenemos el flujo para no gastar recursos
    if not candidatos:
        return {
            "estado": "DETENIDO_AHORRO",
            "mensaje": "Concepto no registrado en memoria aislada. Cero gasto adicional."
        }

    # Paso 3: Ordenamiento por Mínima Acción (menor valor de accion_s primero)
    candidatos.sort(key=lambda item: item["accion_s"])
    mejor_ruta = candidatos[0]

    # Paso 4: Enrutamiento según umbral de entropía (MonitorEntropia)
    if mejor_ruta["entropia"] <= UMBRAL_ENTROPIA:
        mejor_ruta["estado"] = "SISTEMA_1_OPTIMO"
    else:
        mejor_ruta["estado"] = "SISTEMA_1_BAJA_COINCIDENCIA"

    return mejor_ruta


# ==============================================================================
# 4. INTERFAZ DE EJECUCIÓN EN CONSOLA (MODO INTERACTIVO LIGERO)
# ==============================================================================
def iniciar_motor():
    """Punto de entrada principal del programa."""
    print("🔄 Cargando memoria aislada desde GitHub...")
    base = cargar_base_desde_github(URL_BASE_GITHUB)

    if not base:
        return

    meta = base.get("metadatos", {})
    total = len(base.get("conceptos_aislados", {}))
    print(f"✅ Núcleo listo | Autor: {meta.get('autor', 'N/A')}")
    print(f"📦 Conceptos aislados cargados: {total} | Modo: {meta.get('modo_operacion')}")
    print("Escribe tu consulta (o escribe 'salir' para terminar):\n")

    while True:
        consulta = input("🔎 Consulta > ").strip()
        if consulta.lower() in ["salir", "exit", "q"]:
            print("🛑 Ejecución finalizada. Consumo mínimo garantizado.")
            break

        resultado = buscar_y_evaluar_accion(consulta, base)
        print(f"  📌 Estado   : {resultado.get('estado')}")

        if "id" in resultado:
            print(f"  🆔 Concepto : [{resultado['id']}] {resultado['nombre']} ({resultado['tipo']})")
            print(f"  ⚡ Entropía : {resultado['entropia']} | Acción S: {resultado['accion_s']}")
            print(f"  🧩 Sintaxis : {resultado['sintaxis']}")
            print(f"  📖 Detalle  : {resultado['detalle']}\n")
        else:
            print(f"  ℹ️ Aviso    : {resultado.get('mensaje')}\n")


if __name__ == "__main__":
    iniciar_motor()
