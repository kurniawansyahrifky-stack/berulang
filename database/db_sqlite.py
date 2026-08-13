import sqlite3
import config

def get_db():
    conn = sqlite3.connect(config.DB_FILE, timeout=30.0)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    try:
        conn = get_db()
        c = conn.cursor()
        c.execute("PRAGMA journal_mode=WAL;")
        c.execute("""
            CREATE TABLE IF NOT EXISTS periodic_tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT,
                chat_id INTEGER,
                msg_text TEXT,
                photo_path TEXT,
                buttons_json TEXT,
                start_hour INTEGER,
                interval_type TEXT,
                interval_val INTEGER,
                last_msg_id INTEGER,
                status TEXT DEFAULT 'RUNNING'
            )
        """)
        conn.commit()
        conn.close()
        print(f"📦 Database SQLite Terisolasi aktif di: {config.DB_FILE}")
    except Exception as e:
        print(f"❌ Gagal menginisialisasi database: {e}")
