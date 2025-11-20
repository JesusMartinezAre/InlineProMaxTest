import serial
import re
import time
from config import PUERTO_LIDAR, BAUDRATE
from threading import Thread
from .lidar_events import handle_zone_enter


def lidar_loop(detener_flag):
    """Hilo principal: lee el LIDAR y dispara eventos de zona."""
    try:
        lidar = serial.Serial(PUERTO_LIDAR, BAUDRATE, timeout=1)
        print(f"[LIDAR] conectado en {PUERTO_LIDAR}")
    except Exception as e:
        print(f"[LIDAR] ERROR apertura: {e}")
        lidar = None

    while not detener_flag["stop"]:
        line = ""

        if lidar:
            try:
                line = lidar.readline().decode("utf-8", errors="ignore").strip()
            except:
                pass

        if not line:
            continue

        print("[LIDAR]", line)

        match = re.search(r"ZONE(\d+)=ENTER", line)
        if match:
            zone = int(match.group(1))
            handle_zone_enter(zone)


def start_lidar_thread(detener_flag):
    t = Thread(target=lidar_loop, args=(detener_flag,), daemon=True)
    t.start()
    return t
