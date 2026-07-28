import platform
import subprocess
import ctypes

def lock_screen():
    system_platform = platform.system()

    if system_platform == "Windows":
        # Windows lock screen command
        ctypes.windll.user32.LockWorkStation()
    elif system_platform == "Darwin":
        # macOS lock screen command
        subprocess.run(["pmset", "displaysleepnow"])
    elif system_platform == "Linux":
        # Linux lock screen command (this may vary depending on the desktop environment)
        subprocess.run(["gnome-screensaver-command", "--lock"])
    else:
        print("Lock screen functionality is not supported on this platform.")

