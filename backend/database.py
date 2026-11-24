"""database.py - SQLite helpers (parameterised queries only)."""
import sqlite3
from datetime import datetime

from config import Config


def get_conn():
    conn = sqlite3.connect(Config.DATABASE_PATH)
    conn.row_factory = sqlite3.Row
    return conn


def init_db():
    Config.DATABASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    conn = get_conn()
    with conn:
        conn.execute("""CREATE TABLE IF NOT EXISTS detection_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            detection_type TEXT NOT NULL CHECK (detection_type IN ('image','webcam')),
            total_faces INTEGER NOT NULL,
            image_filename TEXT,
            detection_date TEXT NOT NULL,
            detection_time TEXT NOT NULL)""")
    conn.close()


def add_record(detection_type, total_faces, image_filename=None):
    now = datetime.now()
    conn = get_conn()
    with conn:
        cur = conn.execute(
            "INSERT INTO detection_history (detection_type,total_faces,image_filename,"
            "detection_date,detection_time) VALUES (?,?,?,?,?)",
            (detection_type, int(total_faces), image_filename,
             now.strftime("%Y-%m-%d"), now.strftime("%H:%M:%S")))
        new_id = cur.lastrowid
    conn.close()
    return new_id


def list_records(limit=None):
    sql, args = "SELECT * FROM detection_history ORDER BY id DESC", ()
    if limit:
        sql, args = sql + " LIMIT ?", (int(limit),)
    conn = get_conn()
    rows = [dict(r) for r in conn.execute(sql, args)]
    conn.close()
    return rows


def delete_record(record_id):
    conn = get_conn()
    with conn:
        deleted = conn.execute("DELETE FROM detection_history WHERE id=?", (record_id,)).rowcount > 0
    conn.close()
    return deleted


def get_statistics():
    conn = get_conn()
    r = conn.execute("""SELECT COALESCE(SUM(total_faces),0) f, COUNT(*) s,
        COALESCE(SUM(detection_type='image'),0) i,
        COALESCE(SUM(detection_type='webcam'),0) w FROM detection_history""").fetchone()
    conn.close()
    return {"total_faces": r["f"], "total_sessions": r["s"],
            "image_detections": r["i"], "webcam_detections": r["w"],
            "recent": list_records(5)}
