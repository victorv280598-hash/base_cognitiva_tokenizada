"""
==============================================================================
PROYECTO: Sistema Cognitivo LLM - Núcleo Aislado de Mínima Acción
REPOSITORIO: https://github.com/victorv280598-hash/base_cognitiva_tokenizada
ARCHIVO: agregar_concepto.py
AUTOR: Victor Jose Vazquez Preciado
LICENCIA: Todos los derechos reservados (All Rights Reserved).
DESCRIPCIÓN: Herramienta ligera en Python puro para añadir nuevos conceptos
aislados a 'base_cognitiva_tokenizada.json', calculando sus tokens
automáticamente sin gasto computacional externo.
==============================================================================
"""

import json
import re
from datetime import datetime

# ==============================================================================
# 1. PARÁMETROS AJUSTABLES DEL SISTEMA
# ==============================================================================
ARCHIVO_BASE_JSON = "base_cognitiva_tokenizada.json"
PATRON_TOKENS = r'[\w-]+|[#$&\[\]]'  # Conserva palabras y símbolos (#, $, &, [, ])


# ==============================================================================
# 2. FUNCIONES DE LECTURA, TOKENIZACIÓN Y GUARDADO
# ==============================================================================
def tokenizar_texto(texto: str) -> list[str]:
    """
    Extrae palabras y símbolos clave en minúsculas.
    Operación determinista O(n) de consumo energético mínimo.
    """
    return re.findall(PATRON_TOKENS, texto.lower())


def cargar_base_local(ruta: str) -> dict:
    """Lee el archivo JSON actual desde el repositorio."""
    try:
        with open(ruta, "r", encoding="utf-8") as archivo:
            return json.load(archivo)
    except FileNotFoundError:
        print(f"⚠️ No se encontró '{ruta}'. Asegúrate de estar en la carpeta raíz del repositorio.")
        return {}
    except json.JSONDecodeError as error:
        print(f"⚠️ El archivo '{ruta}' tiene un error de formato JSON: {error}")
        return {}


def procesar_y_agregar(base: dict, id_concepto: str, tipo: str, nombre: str, detalle: str, sintaxis: str) -> dict:
    """
    Aísla el nuevo concepto bajo su ID, calcula sus métricas de tokens
    y actualiza los metadatos globales de la base.
    """
    id_limpio = id_concepto.strip().upper()
    texto_indexable = f"{id_limpio} {tipo} {nombre} {detalle} {sintaxis}"

    todos_los_tokens = tokenizar_texto(texto_indexable)
    tokens_unicos = sorted(list(set(todos_los_tokens)))

    # Insertamos el bloque aislado en el diccionario principal
    base["conceptos_aislados"][id_limpio] = {
        "tipo": tipo.strip(),
        "nombre": nombre.strip(),
        "detalle": detalle.strip(),
        "sintaxis": sintaxis.strip(),
        "metricas_tokens": {
            "cantidad_total": len(todos_los_tokens),
            "tokens_unicos": tokens_unicos
        }
    }

    # Actualizamos metadatos de control
    base["metadatos"]["ultima_actualizacion"] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    base["metadatos"]["total_conceptos"] = len(base["conceptos_aislados"])

    return base


def guardar_base_local(ruta: str, base: dict) -> None:
    """Guarda el diccionario actualizado en formato JSON legible."""
    with open(ruta, "w", encoding="utf-8") as archivo:
        json.dump(base, archivo, ensure_ascii=False, indent=2)


# ==============================================================================
# 3. INTERFAZ INTERACTIVA EN CONSOLA (OPTIMIZADA PARA MÓVIL)
# ==============================================================================
def iniciar_asistente_insercion():
    """Guía paso a paso para agregar conceptos aislados desde la terminal."""
    base = cargar_base_local(ARCHIVO_BASE_JSON)
    if not base:
        return

    print("=================================================================")
    print("📦 ASISTENTE DE AISLAMIENTO Y TOKENIZACIÓN DE CONCEPTOS")
    print(f"Conceptos actuales en la base: {len(base.get('conceptos_aislados', {}))}")
    print("Escribe 'salir' en el ID cuando termines de agregar conceptos.")
    print("=================================================================\n")

    while True:
        id_nuevo = input("1. ID único (ej. LEY-03, SIS-01, LLM-003) > ").strip()
        if id_nuevo.lower() in ["salir", "exit", "q"]:
            break
        if not id_nuevo:
            print("⚠️ El ID no puede estar vacío.\n")
            continue

        if id_nuevo.upper() in base["conceptos_aislados"]:
            sobrescribir = input(f"⚠️ El ID '{id_nuevo.upper()}' ya existe. ¿Reemplazar? (s/n) > ").strip().lower()
            if sobrescribir != "s":
                print("Operación cancelada.\n")
                continue

        tipo = input("2. Tipo (ej. Ley Logica, Sistema Modal, Simbolo, Estructura Prompt) > ").strip()
        nombre = input("3. Nombre del concepto (ej. De Morgan 3, Few-Shot) > ").strip()
        detalle = input("4. Detalle o definición breve > ").strip()
        sintaxis = input("5. Sintaxis simbólica (ej. [# \"Nombre\" $regla [\"...\"];]) > ").strip()

        base = procesar_y_agregar(base, id_nuevo, tipo, nombre, detalle, sintaxis)
        guardar_base_local(ARCHIVO_BASE_JSON, base)

        info_guardada = base["conceptos_aislados"][id_nuevo.upper()]
        print(f"\n✅ Concepto [{id_nuevo.upper()}] aislado y guardado.")
        print(f"   Tokens generados ({info_guardada['metricas_tokens']['cantidad_total']}): {info_guardada['metricas_tokens']['tokens_unicos']}\n")

    print("\n🛑 Sesión finalizada. Recuerda hacer 'Commit & Push' en GitHub para sincronizar tus cambios.")


if __name__ == "__main__":
    iniciar_asistente_insercion()
