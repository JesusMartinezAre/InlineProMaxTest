import os
import pygame
from config import AUDIO_DIR, MODO_AUDIOS

def get_audio_for_zone(zone, columna):
    if MODO_AUDIOS == "zona":
        candidate = os.path.join(AUDIO_DIR, f"{zone}.wav")
        if os.path.exists(candidate):
            return candidate

    candidate = os.path.join(AUDIO_DIR, f"columna{columna}.wav")
    if os.path.exists(candidate):
        return candidate

    return None


def play_audio(path):
    try:
        sound = pygame.mixer.Sound(path)
        pygame.mixer.Channel(0).stop()
        pygame.mixer.Channel(0).play(sound)
        print(f"[AUDIO] Reproduciendo {path}")
    except Exception as e:
        print(f"[AUDIO] Error: {e}")
