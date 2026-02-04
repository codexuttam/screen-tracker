import sys
import sqlite3
from datetime import date, timedelta

DB_NAME = "/home/codebloodedsash/my-screen-tracker/usage.db"

def format_time(seconds):
    hours = seconds // 3600
    minutes = (seconds % 3600) // 60
    return hours, minutes

def main():
    # Default: today
    report_date = date.today().isoformat()

    if len(sys.argv) > 1:
        if sys.argv[1] == "yesterday":
            report_date = (date.today() - timedelta(days=1)).isoformat()
        else:
            report_date = sys.argv[1]  # YYYY-MM-DD

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT app_name, seconds_used
        FROM app_usage
        WHERE date = ?
        ORDER BY seconds_used DESC
    """, (report_date,))

    rows = cursor.fetchall()
    conn.close()

    if not rows:
        print(f"📭 No screen time recorded for {report_date}.")
        return

    print(f"\n📅 Screen Time Report ({report_date})\n")

    total = 0
    for app, seconds in rows:
        h, m = format_time(seconds)
        total += seconds
        print(f"{app:12} : {h}h {m}m")

    th, tm = format_time(total)
    print("\n" + "-" * 26)
    print(f"Total        : {th}h {tm}m\n")

if __name__ == "__main__":
    main()
