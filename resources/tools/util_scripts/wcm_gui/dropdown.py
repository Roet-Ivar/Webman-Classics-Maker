try:
    # Python2
    import Tkinter as tk
    import ttk
except ImportError as e:
    # Python3
    import tkinter as tk
    from tkinter import ttk

class DriveDropdown:
    def __init__(self, root, frame, x, y):
        # disabled PSP for now
        self.root = root
        self.frame = frame
        self.combobox = ttk.Combobox(root, values=["ALL", "HDD0", "USB(*)", "USB000", "USB001", "USB002", "USB003"], name="drive_dropdown")
        self.combobox.place(x=x, y=y)
        self.combobox.current(0)
        self.combobox.config(width='7', state="readonly")

    def get_box(self):
        return self.combobox

class PlatformDropdown:
    def __init__(self, root, frame, x, y):
        self.root = root
        self.frame = frame
        self.combobox = ttk.Combobox(root, values=["ALL", "PSPISO", "PSXISO", "PS2ISO", "PS3ISO", 'NTFS', "GAMES"], name="platform_dropdown")
        self.combobox.place(x=x, y=y)
        self.combobox.current(0)
        self.combobox.config(width='7', state="readonly")

    def get_box(self):
        return self.combobox


