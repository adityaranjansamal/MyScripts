Battery Alert Script
====================

Overview
--------
This script monitors the laptop battery percentage and shows a fullscreen popup alert when the battery level is low or safely charged.  
It also plays a custom sound at maximum volume until the user dismisses the popup manually.

- Shows alert when battery level is 25% or below.  
- Shows alert when battery level reaches 80% or more while charging.  
- Plays custom looping sound until dismissed.  
- Popup has a "Dismiss" button to close it.  
- Runs continuously in the background.  

File Structure
--------------
battery-alert/  
│  
├── battery_alert.py        (Main script)  
├── low.mp3                 (Custom sound for low battery)  
├── charged.mp3             (Custom sound for safely charged)  
└── README.txt              (Documentation)  

Dependencies
------------
Install the required packages before running the script:

    pip install psutil pygame pycaw comtypes

Python 3.8 or later is recommended.  

Usage
-----
Run manually:

    python battery_alert.py

Run without console window:

    pythonw battery_alert.py

The script checks the battery percentage every 60 seconds and displays alerts when thresholds are reached.  

Autostart with Windows
----------------------
To make the script run automatically at login:

1. Create a shortcut with target:

       pythonw.exe "C:\path\to\battery_alert.py"

   Replace with the correct path to your Python installation and script file.

2. Place the shortcut in the Startup folder:
   - Press Win + R, type:

         shell:startup

   - Paste the shortcut there.  

Help
----
- Low battery sound: Replace low.mp3 with any audio file you prefer.  
- Charged sound: Replace charged.mp3 with your preferred audio file.  
- Thresholds: Change LOW_BATTERY_THRESHOLD and SAFE_CHARGED_THRESHOLD at the top of battery_alert.py.  
- Check interval: Adjust CHECK_INTERVAL (in seconds) to change how often the battery is checked.  
