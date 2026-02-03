import subprocess
import time
import psutil
from collections import defaultdict

CHECK_INTERVAL = 5
IDLE_THRESHOLD_MS = 60000  # 60 seconds

usage = defaultdict(int)
last_app = None


def get_idle_time():
    try:
        return int(subprocess.check_output(["xprintidle"]).decode().strip())
    except:
        return 0


def get_active_window():
    try:
        window_id_dec = int(
            subprocess.check_output(["xdotool", "getactivewindow"])
            .decode()
            .strip()
        )
        window_id_hex = f"0x{window_id_dec:08x}"

        for line in subprocess.check_output(["wmctrl", "-lp"]).decode().splitlines():
            parts = line.split(None, 4)
            if parts[0].lower() == window_id_hex:
                pid = int(parts[2])
                app = psutil.Process(pid).name()
                return app
    except:
        pass
    return None


print("⏱️ Screen Time Tracker Started (Ctrl+C to stop)\n")

try:
    while True:
        idle = get_idle_time()

        if idle < IDLE_THRESHOLD_MS:
            app = get_active_window()
            if app:
                usage[app] += CHECK_INTERVAL
                print(f"Tracking: {app}")

        time.sleep(CHECK_INTERVAL)

except KeyboardInterrupt:
    print("\n📊 Session Summary:\n")
    for app, seconds in usage.items():
        mins = seconds // 60
        secs = seconds % 60
        print(f"{app:20} : {mins} min {secs} sec")
    print("\n👋 Tracker stopped cleanly.")

