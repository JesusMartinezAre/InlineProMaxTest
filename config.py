import os

# ========== PUERTOS ==========
PUERTO_LIDAR = "COM8"
PUERTO_ESP32 = "COM7"
BAUDRATE = 115200

# ========== RUTAS Y DIRECTORIOS ==========
BASE_DIR = os.path.dirname(__file__)
VIDEO_DIR = os.path.join(BASE_DIR, "videos")
AUDIO_DIR = os.path.join(BASE_DIR, "audio")

VIDEO_BASE_FILE = os.path.join(VIDEO_DIR, "base.mp4")
CENEFA_FILE = os.path.join(VIDEO_DIR, "cenefa.mp4")
COPETE_FILE = os.path.join(VIDEO_DIR, "Copete.mp4")

# ========== MODOS ==========
MODO_VIDEOS = "zona"
MODO_AUDIOS = "columna"

VELOCIDAD_VIDEO = 1.0
TIEMPO_INACTIVIDAD = 5.0

# ========== MAPEO ZONA → LED ==========
zona_a_led = {
    1: (-1, 0), 2: (-1, 1), 3: (-1, 2),
    4: (0, 0),  5: (0, 1),  6: (0, 2),
    7: (1, 0),  8: (1, 1),  9: (1, 2),
    10: (2, 0), 11: (2, 1), 12: (2, 2),
    13: (3, 0), 14: (3, 1), 15: (3, 2),
    16: (4, 0), 17: (4, 1), 18: (4, 2)
}

colores = {
    0: (255, 0, 0),
    1: (0, 0, 255),
    2: (0, 255, 0)
}

animacion = 4

# ========== POSICIONES CENEFAS ==========
CENEFA_POS = {
    1: (0, 0, 640, 128),
    2: (640, 0, 640, 128),
    3: (1280, 0, 640, 128),
    4: (0, 128, 800, 40),
    5: (800, 128, 800, 40),
    6: (0, 168, 800, 40),
    7: (800, 208, 800, 40),
    8: (0, 208, 800, 40),
    9: (800, 168, 800, 40),
    10: (0, 248, 800, 40),
    11: (800, 248, 800, 40),
    12: (0, 288, 800, 40),
    13: (800, 328, 800, 40),
    14: (0, 328, 800, 40),
    15: (800, 288, 800, 40),
    16: (0, 368, 800, 40),
    17: (800, 368, 800, 40),
    18: (0, 408, 800, 40),
    19: (0, 0, 1920, 128)
}

