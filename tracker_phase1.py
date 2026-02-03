import subprocess
import time
import psutil

def get_active_window():
    try:
        # Get active window ID (decimal)
        window_id_dec = int(
            subprocess.check_output(["xdotool", "getactivewindow"])
            .decode()
            .strip()
        )

        # Convert to wmctrl-style hex (0x00abcdef)
        window_id_hex = f"0x{window_id_dec:08x}"

        window_list = subprocess.check_output(
            ["wmctrl", "-lp"]
        ).decode().splitlines()

        for line in window_list:
            parts = line.split(None, 4)
            if parts[0].lower() == window_id_hex:
                pid = int(parts[2])
                process = psutil.Process(pid)
                app_name = process.name()
                window_title = parts[4] if len(parts) > 4 else ""
                return app_name, window_title

    except Exception as e:
        pass

    return None, None


if __name__ == "__main__":
    print("🖥️ Screen Tracker Started (Ctrl+C to stop)\n")

    while True:
        app, title = get_active_window()
        if app:
            print(f"Active App: {app} | Window: {title}")
        else:
            print("No active window detected")

        time.sleep(5)
