import os
import cv2
from config import VIDEO_DIR, CENEFA_FILE, COPETE_FILE

def get_video_for_zone(zone):
    zone = int(zone)

    zone_videos = {
        1: "cenefa1.mp4", 2: "cenefa1.mp4", 3: "cenefa1.mp4",
        4: "cenefa1.mp4", 5: "cenefa2.mp4", 6: "cenefa3.mp4",
        7: "cenefa4.mp4", 8: "cenefa5.mp4", 9: "cenefa6.mp4",
        10: "cenefa7.mp4", 11: "cenefa8.mp4", 12: "cenefa9.mp4",
        13: "cenefa10.mp4", 14: "cenefa11.mp4", 15: "cenefa1.mp4",
        16: "cenefa2.mp4", 17: "cenefa3.mp4", 18: "cenefa4.mp4",
        19: "Copete.mp4"
    }

    filename = zone_videos.get(zone, "cenefa.mp4")
    path = os.path.join(VIDEO_DIR, filename)

    if not os.path.exists(path):
        print(f"[WARN] {path} no existe, usando fallback {CENEFA_FILE}")
        return CENEFA_FILE

    return path


def open_capture_safe(path):
    """Abre un VideoCapture seguro y devuelve None si falla."""
    if not os.path.exists(path):
        print(f"[ERROR] No existe: {path}")
        return None

    cap = cv2.VideoCapture(path)
    if not cap.isOpened():
        print(f"[ERROR] Falló al abrir: {path}")
        return None

    return cap
