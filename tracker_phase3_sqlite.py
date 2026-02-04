import subprocess
import time
import psutil
import sqlite3
from datetime import date

CHECK_INTERVAL = 5
IDLE_THRESHOLD_MS = 60000
DB_NAME = "usage.db"


def setup_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute("""
        CREATE TABLE IF NOT EXISTS app_usage (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            app_name TEXT,
            date TEXT,
            seconds_used INTEGER
        )
    """)
    conn.commit()
    conn.close()


def get_idle_time():
    try:
        return int(subprocess.check_output(["xprintidle"]).decode())
    except:
        return 0

def get_active_app():
    try:
        pid = subprocess.check_output(
            ["xdotool", "getwindowfocus", "getwindowpid"]
        ).decode().strip()
        return psutil.Process(int(pid)).name().replace(".exe", "")
    except Exception:
        return None



def log_time(app):
    today = date.today().isoformat()
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()

    c.execute("""
        SELECT seconds_used FROM app_usage
        WHERE app_name=? AND date=?
    """, (app, today))

    row = c.fetchone()
    if row:
        c.execute("""
            UPDATE app_usage
            SET seconds_used = seconds_used + ?
            WHERE app_name=? AND date=?
        """, (CHECK_INTERVAL, app, today))
    else:
        c.execute("""
            INSERT INTO app_usage (app_name, date, seconds_used)
            VALUES (?, ?, ?)
        """, (app, today, CHECK_INTERVAL))

    conn.commit()
    conn.close()


print("📊 Persistent Screen Time Tracker Started\n")
setup_db()

try:
    while True:
        if get_idle_time() < IDLE_THRESHOLD_MS:
            app = get_active_app()
            if app:
                log_time(app)
                print(f"Logged: {app}")
        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n👋 Tracker stopped cleanly.")
