# core/lidar_manager.py
import serial
import time
import threading
import re
import sys

from config import PUERTO_LIDAR  # si existe en tu config; si no, se usa autodetección
from utils.video_utils import get_video_for_zone
from core.zone_manager import (
    activate_zone,
    release_zone,
    update_zone_timestamp
)

# ------------------------------------------------------------
# Config puerto: usa PUERTO_LIDAR si está en config, si no autodetecta
# ------------------------------------------------------------
def _detectar_puerto_default():
    if 'PUERTO_LIDAR' in globals() or 'PUERTO_LIDAR' in locals():
        return PUERTO_LIDAR
    if sys.platform.startswith("win"):
        # si config no define PUERTO_LIDAR, puedes ajustar aquí el COM por defecto
        return "COM8"
    else:
        return "/dev/ttyUSB0"

try:
    SERIAL_PORT = PUERTO_LIDAR
except Exception:
    SERIAL_PORT = _detectar_puerto_default()

BAUDRATE = 115200

# Regex para capturar: ZONE03=ENTER o ZONE01=EXIT (soporta prefijos y sufijos)
PATRON_EVENTO = re.compile(r"ZONE\s*0*?(\d+)\s*\=\s*(ENTER|EXIT)", re.IGNORECASE)
# soporta: ZONE03=ENTER, ZONE3 = ENTER, ZONE03 = enter, etc.


def procesar_linea_lidar(linea: str):
    """Extrae (zona, evento) o (None, None) si no corresponde."""
    if not linea:
        return None, None
    m = PATRON_EVENTO.search(linea)
    if not m:
        return None, None
    zona = int(m.group(1))
    evento = m.group(2).upper()
    return zona, evento


def manejar_evento_zona(zona: int, evento: str):
    """Integra el evento con zone_manager usando las rutas reales de video."""
    if evento == "ENTER":
        # obtener la ruta real para la zona (usa tu mapeo existente)
        ruta = get_video_for_zone(zona)
        if ruta is None:
            print(f"[LIDAR] No se encontró video para zona {zona}")
            return
        # activar la zona con la ruta real
        activate_zone(zona, ruta)
        update_zone_timestamp(zona)
    else:  # EXIT
        release_zone(zona)

    print(f"[LIDAR] Zona {zona} -> {evento}")


def lidar_loop(detener_flag: dict):
    """Loop que lee el puerto serial y procesa líneas completas."""
    print(f"[LIDAR] Iniciando lectura en {SERIAL_PORT}...")
    try:
        ser = serial.Serial(SERIAL_PORT, BAUDRATE, timeout=0.1)
    except Exception as e:
        print(f"[LIDAR] ERROR al abrir puerto {SERIAL_PORT}: {e}")
        return

    buffer = ""
    while not detener_flag.get("stop", False):
        try:
            data = ser.read().decode(errors="ignore")
        except Exception:
            # si falla la lectura temporalmente, seguimos
            time.sleep(0.01)
            continue

        if not data:
            continue

        buffer += data
        # procesar líneas completas
        if "\n" not in buffer:
            continue

        partes = buffer.split("\n")
        buffer = partes[-1]  # fragmento final incompleto
        lineas = partes[:-1]

        for linea in lineas:
            linea = linea.strip()
            if not linea:
                continue
            zona, evento = procesar_linea_lidar(linea)
            if zona is None:
                # si la línea tiene formato diferente (p.ej. X001B[ZONE03=ENTER]), intentar extraer parte interna
                # ejemplo: buscar substring "ZONE"
                possible = re.search(r"ZONE.*?=", linea, re.IGNORECASE)
                if possible:
                    zona, evento = procesar_linea_lidar(linea)
                if zona is None:
                    # no corresponde, ignorar
                    continue
            try:
                manejar_evento_zona(zona, evento)
            except Exception as e:
                print(f"[LIDAR] Error manejando evento zona {zona}: {e}")

    print("[LIDAR] Detenido.")
    try:
        ser.close()
    except:
        pass


def start_lidar_thread(detener_flag: dict):
    t = threading.Thread(target=lidar_loop, args=(detener_flag,), daemon=True)
    t.start()
    return t
