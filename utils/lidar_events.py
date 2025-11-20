# utils/lidar_events.py
import time
from config import CENEFA_POS, animacion, zona_a_led
from utils.video_utils import get_video_for_zone, open_capture_safe
from utils.audio_utils import get_audio_for_zone, play_audio
from utils.esp32_utils import esp32_write
from utils.helpers import obtener_color_por_columna
from utils.pygame_utils import video_lock, active_zones, zone_last_seen, zone_caps

def handle_zone_enter(zone):
    """
    Lógica que ocurre cuando el LIDAR reporta ZONEX=ENTER.
    - activa la zona
    - abre capture si hace falta
    - activa la zona 19 (copete) si zone in 1..18
    - envía comando al ESP32 si la zona está mapeada
    - reproduce audio si existe
    """
    try:
        zone = int(zone)
    except Exception:
        print(f"[LIDAR_EVENT] Zona inválida: {zone}")
        return

    if zone not in CENEFA_POS:
        print(f"[WARN] Zona {zone} fuera de mapeo CENEFA_POS")
        return

    # marcar y abrir capture para la zona
    with video_lock:
        active_zones.add(zone)
        zone_last_seen[zone] = time.time()

        if zone not in zone_caps or zone_caps.get(zone) is None:
            ruta = get_video_for_zone(zone)
            cap = open_capture_safe(ruta)
            zone_caps[zone] = cap
            if cap:
                print(f"[ZONE] Abierto video {ruta} para zona {zone}")

    # si se activa una zona 1..18, también activar la 19 (copete)
    if 1 <= zone <= 18:
        with video_lock:
            active_zones.add(19)
            zone_last_seen[19] = time.time()
            if 19 not in zone_caps or zone_caps.get(19) is None:
                ruta19 = get_video_for_zone(19)  # normalmente COPETE_FILE
                cap19 = open_capture_safe(ruta19)
                zone_caps[19] = cap19
                if cap19:
                    print(f"[ZONE] Abierto copete {ruta19} para zona 19")

    # enviar comando ESP32 si está mapeada
    if zone in zona_a_led:
        fila, columna = zona_a_led[zone]
        r, g, b = obtener_color_por_columna(columna)
        comando = f"{fila},{columna},{r},{g},{b},{animacion}\n"
        try:
            esp32_write(comando)
            print(f"[ESP32] Enviado: {comando.strip()}")
        except Exception as e:
            print(f"[ESP32] Error enviando comando: {e}")

    # reproducir audio si existe
    try:
        if zone in zona_a_led:
            _, columna = zona_a_led[zone]
        else:
            columna = 0
        ruta_audio = get_audio_for_zone(zone, columna)
        if ruta_audio:
            play_audio(ruta_audio)
    except Exception as e:
        print(f"[AUDIO] Error al reproducir audio: {e}")
