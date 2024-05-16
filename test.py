import platform

def get_active_window():
    active_window_name = "[COULD NOT BE DETERMINED]"
    if platform.system() == "Linux":
        try:
            import wnck
            screen = wnck.screen_get_default()
            screen.force_update()
            window = screen.get_active_window()
            if window is not None:
                pid = window.get_pid()
                with open(f"/proc/{pid}/cmdline") as f:
                    active_window_name = f.read()
        except Exception as e:
            print(e)
            raise
    elif platform.system() == "Windows":
        try:
            import win32gui
            window = win32gui.GetForegroundWindow()
            active_window_name = win32gui.GetWindowText(window)
        except Exception as e:
            print(e)
            raise
    elif platform.system() == "Darwin":
        try:
            from AppKit import NSWorkspace
            active_window_name = (
                NSWorkspace.sharedWorkspace().activeApplication()["NSApplicationName"]
            )
        except Exception as e:
            print(e)
            raise
    return active_window_name

while True:
    print(get_active_window())