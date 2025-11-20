import serial
from config import PUERTO_ESP32, BAUDRATE
import threading

esp32_serial = None
esp32_lock = threading.Lock()


def esp32_init():
    global esp32_serial
    try:
        esp32_serial = serial.Serial(PUERTO_ESP32, BAUDRATE, timeout=1)
        print(f"[ESP32] Conectado en {PUERTO_ESP32}")
    except Exception as e:
        print(f"[ESP32] No se pudo abrir: {e}")
        esp32_serial = None


def esp32_write(cmd):
    global esp32_serial
    with esp32_lock:
        if esp32_serial:
            esp32_serial.write(cmd.encode())
        else:
            try:
                tmp = serial.Serial(PUERTO_ESP32, BAUDRATE, timeout=0.5)
                tmp.write(cmd.encode())
                tmp.close()
            except Exception as e:
                print(f"[ESP32] ERROR temporal: {e}")
