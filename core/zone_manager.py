import time 

from utils.pygame_utils import (
    video_lock,
    active_zones,
    zone_last_seen,
    zone_caps
)

from utils.video_utils import open_capture_safe


def activate_zone(zone, video_file):
    """Activa la zona y abre el video correspondiente."""
    with video_lock:
        cap = open_capture_safe(video_file)
        zone_caps[zone] = cap
        active_zones.add(zone)
        zone_last_seen[zone] = time.time()

    print(f"[ZONE] Activada zona {zone} → {video_file}")


def update_zone_timestamp(zone):
    """Renueva el tiempo de última detección."""
    with video_lock:
        zone_last_seen[zone] = time.time()


def release_zone(zone):
    """Cierra el video y elimina la zona."""
    with video_lock:
        if zone in active_zones:
            active_zones.remove(zone)

        cap = zone_caps.get(zone)
        if cap:
            cap.release()
        zone_caps[zone] = None

        if zone in zone_last_seen:
            zone_last_seen.pop(zone)

    print(f"[ZONE] Zona {zone} liberada")


def release_all():
    """Cierra TODAS las zonas cuando se apaga el programa."""
    with video_lock:
        for z, cap in zone_caps.items():
            if cap:
                cap.release()
            zone_caps[z] = None

        active_zones.clear()
        zone_last_seen.clear()

    print("[ZONE] Todas las zonas liberadas")
