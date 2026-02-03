# 🖥️ Linux Screen Time Tracker

A lightweight Ubuntu-based screen time tracker that monitors:
- Total active screen time
- Per-application usage
- Idle-aware tracking

Built from scratch using Python and Linux system utilities.

---

## 🚀 Features
- Tracks active window & application
- Counts real usage time (ignores idle time)
- Stores data locally using SQLite
- Simple, extendable architecture

---

## 🛠️ Tech Stack
- Python
- SQLite
- wmctrl
- xdotool
- psutil

---

## ⚙️ Installation

```bash
sudo apt install wmctrl xdotool xprintidle
pip install -r requirements.txt
