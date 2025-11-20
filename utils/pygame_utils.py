import pygame
import cv2
import time
from threading import Lock
from config import VIDEO_BASE_FILE, CENEFA_POS, TIEMPO_INACTIVIDAD
from .video_utils import open_capture_safe
from .helpers import cv2frame_to_surface

video_lock = Lock()

active_zones = set()
zone_last_seen = {}
zone_caps = {}

def start_pygame_window():
    pygame.init()
    if not pygame.mixer.get_init():
        pygame.mixer.init()

    screen = pygame.display.set_mode((1920, 1080))
    pygame.display.set_caption("Control Cenefas")

    return screen


def render_loop(detener_flag):
    screen = start_pygame_window()
    clock = pygame.time.Clock()

    base_cap = open_capture_safe(VIDEO_BASE_FILE)
    base_fallback = pygame.Surface((1920, 1080))
    base_fallback.fill((0, 255, 0))

    last_base = time.time()

    while not detener_flag["stop"]:
        # Eventos
        for ev in pygame.event.get():
            if ev.type == pygame.QUIT:
                detener_flag["stop"] = True
            elif ev.type == pygame.KEYDOWN and ev.key == pygame.K_q:
                detener_flag["stop"] = True

        # FRAME BASE
        if base_cap:
            ret, frame = base_cap.read()
            if not ret:
                base_cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                ret, frame = base_cap.read()

            if ret:
                surf = cv2frame_to_surface(frame)
                if surf:
                    screen.blit(surf, (0, 0))
            else:
                screen.blit(base_fallback, (0, 0))
        else:
            screen.blit(base_fallback, (0, 0))

        # OVERLAYS
        with video_lock:
            zones_snapshot = list(active_zones)

        for z in zones_snapshot:
            cap = zone_caps.get(z)

            if cap:
                ret, frame_c = cap.read()
                if not ret:
                    cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
                    ret, frame_c = cap.read()

                if ret:
                    x, y, w, h = CENEFA_POS[z]
                    frame_c = cv2.resize(frame_c, (w, h))
                    surf = cv2frame_to_surface(frame_c)
                    if surf:
                        screen.blit(surf, (x, y))

        # TIMEOUTS
        now = time.time()
        with video_lock:
            for z, t in list(zone_last_seen.items()):
                if now - t > TIEMPO_INACTIVIDAD:
                    active_zones.discard(z)
                    cap = zone_caps.get(z)
                    if cap:
                        cap.release()
                    zone_caps[z] = None
                    zone_last_seen.pop(z, None)
                    print(f"[TIMEOUT] Zona {z} eliminada")

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()
    print("[VISUAL] Terminado")
