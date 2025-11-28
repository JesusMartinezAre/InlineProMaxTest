import sqlite3
import threading
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "AnaliticsDB.db")
DB_PATH = os.path.abspath(DB_PATH)

_lock = threading.Lock()


class LocalDB:
    def __init__(self, db_path=DB_PATH):
        self.db_path = db_path
        print("[DB] Usando base de datos en:", self.db_path)
        self._ensure_tables_exist()

    def _connect(self):
        return sqlite3.connect(self.db_path)

    def _ensure_tables_exist(self):
        """Por si borras la DB accidentalmente, recrea la tabla automáticamente."""
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("""
                CREATE TABLE IF NOT EXISTS interactions (
                    interaction_id INTEGER PRIMARY KEY AUTOINCREMENT,
                    zone_number INTEGER NOT NULL,
                    event_datetime DATETIME NOT NULL,
                    synced INTEGER DEFAULT 0
                );
            """)
            con.commit()

    def insert_interaction(self, zone_number: int):
        """Guarda un toque en una zona."""
        event_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        with _lock:
            with self._connect() as con:
                cur = con.cursor()
                cur.execute("""
                    INSERT INTO interactions (zone_number, event_datetime, synced)
                    VALUES (?, ?, 0)
                """, (zone_number, event_time))
                con.commit()

    def get_unsynced(self, limit=100):
        """Obtiene interacciones que aún no se han subido al servidor."""
        with self._connect() as con:
            cur = con.cursor()
            cur.execute("""
                SELECT interaction_id, zone_number, event_datetime
                FROM interactions
                WHERE synced = 0
                ORDER BY interaction_id ASC
                LIMIT ?
            """, (limit,))
            return cur.fetchall()

    def mark_as_synced(self, interaction_id: int):
        """Marca una interacción como sincronizada."""
        with _lock:
            with self._connect() as con:
                cur = con.cursor()
                cur.execute("""
                    UPDATE interactions SET synced = 1
                    WHERE interaction_id = ?
                """, (interaction_id,))
                con.commit()
