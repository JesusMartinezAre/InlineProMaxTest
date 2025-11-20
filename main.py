# main.py
import threading
import time
from utils.esp32_utils import esp32_init
from core.lidar_manager import start_lidar_thread
from core.visual_manager import render_loop
from core import zone_manager

def main():
    detener_flag = {"stop": False}

    esp32_init()

    # iniciar visual
    visual_thread = threading.Thread(target=render_loop, args=(detener_flag,), daemon=True)
    visual_thread.start()

    # iniciar lidar
    lidar_thread = start_lidar_thread(detener_flag)

    try:
        while not detener_flag["stop"]:
            time.sleep(0.2)
    except KeyboardInterrupt:
        detener_flag["stop"] = True

    # limpiar estado
    zone_manager.release_all()
    time.sleep(0.5)
    print("[MAIN] Programa terminado.")

if __name__ == "__main__":
    main()
