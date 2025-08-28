import psutil
import tkinter as tk
from tkinter import messagebox
import pygame
import time
from ctypes import POINTER, cast
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

# ========== SETTINGS ==========
LOW_BATTERY_THRESHOLD = 25
SAFE_CHARGED_THRESHOLD = 81
LOW_BATTERY_SOUND = "low.mp3"
SAFE_CHARGED_SOUND = "charged.mp3"
CHECK_INTERVAL = 120  # seconds
# ==============================

def set_full_volume():
    devices = AudioUtilities.GetSpeakers()
    interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
    volume = cast(interface, POINTER(IAudioEndpointVolume))
    volume.SetMasterVolumeLevelScalar(1.0, None)  # 1.0 = 100%

def play_sound(file):
    pygame.mixer.init()
    set_full_volume()
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(-1)  # loop until dismissed

def stop_sound():
    pygame.mixer.music.stop()

def show_popup(message, soundfile):
    # Tkinter fullscreen popup
    root = tk.Tk()
    root.attributes("-fullscreen", True)
    root.configure(bg="black")

    # Centered label
    label = tk.Label(root, text=message, font=("Arial", 50, "bold"), fg="white", bg="black")
    label.pack(expand=True)

    # Dismiss button
    dismiss_btn = tk.Button(root, text="Dismiss", font=("Arial", 30), command=lambda: (stop_sound(), root.destroy()))
    dismiss_btn.pack(pady=50)

    # Play sound
    play_sound(soundfile)

    root.mainloop()

def monitor_battery():
    while True:
        battery = psutil.sensors_battery()
        percent = battery.percent

        if percent <= LOW_BATTERY_THRESHOLD:
            show_popup("⚠ Battery Low", LOW_BATTERY_SOUND)

        elif percent >= SAFE_CHARGED_THRESHOLD and battery.power_plugged:
            show_popup("🔋 Battery Safely Charged", SAFE_CHARGED_SOUND)

        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    monitor_battery()
