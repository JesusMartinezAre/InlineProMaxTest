import cv2
import pygame
from config import colores

def obtener_color_por_columna(columna):
    return colores.get(columna, (255, 255, 0))


def cv2frame_to_surface(frame):
    """Convierte frame BGR de OpenCV → Surface de pygame."""
    if frame is None:
        return None

    try:
        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        rgb = rgb.swapaxes(0, 1)
        return pygame.surfarray.make_surface(rgb)
    except Exception as e:
        print(f"[HELPERS] Error transformando frame: {e}")
        return None
