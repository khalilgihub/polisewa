import ctypes
import time

user32 = ctypes.windll.user32

def wake_chrome():
    found_windows = []
    
    def enum_windows_proc(hwnd, lParam):
        if user32.IsWindow(hwnd):
            # Check class name
            class_buf = ctypes.create_unicode_buffer(256)
            user32.GetClassNameW(hwnd, class_buf, 256)
            cname = class_buf.value
            
            # Chrome's main window class is Chrome_WidgetWin_1
            if cname == "Chrome_WidgetWin_1":
                length = user32.GetWindowTextLengthW(hwnd)
                if length > 0:
                    title_buf = ctypes.create_unicode_buffer(length + 1)
                    user32.GetWindowTextW(hwnd, title_buf, length + 1)
                    title = title_buf.value
                    if title and not title.startswith("Chrome Legacy"):
                        found_windows.append((hwnd, title))
        return True

    WNDENUMPROC = ctypes.WINFUNCTYPE(ctypes.c_bool, ctypes.c_int, ctypes.c_int)
    user32.EnumWindows(WNDENUMPROC(enum_windows_proc), 0)
    
    print(f"Found {len(found_windows)} Chrome windows:")
    for hwnd, title in found_windows:
        print(f"  HWND: {hwnd} | Title: {title}")
        # Restore window if minimized (SW_RESTORE = 9, SW_SHOW = 5)
        user32.ShowWindow(hwnd, 9)
        # Windows trick to force foreground window:
        # AttachThreadInput of current thread to foreground thread
        fg_hwnd = user32.GetForegroundWindow()
        fg_thread = user32.GetWindowThreadProcessId(fg_hwnd, None)
        curr_thread = user32.GetWindowThreadProcessId(hwnd, None)
        
        user32.AttachThreadInput(curr_thread, fg_thread, True)
        user32.SetForegroundWindow(hwnd)
        user32.BringWindowToTop(hwnd)
        user32.AttachThreadInput(curr_thread, fg_thread, False)
        print("  Brought to foreground!")

if __name__ == "__main__":
    wake_chrome()
