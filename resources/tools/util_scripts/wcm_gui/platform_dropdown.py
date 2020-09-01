try:
    # Python2
    import Tkinter as tk
    import ttk
except ImportError as e:
    print("Tkinter import error: " + e.message)
    # Python3
    import tkinter as tk
    import ttk

class Dropdown:
    def __init__(self, root, frame, x, y):
        # disabled PSP for now
        self.root = root
        self.frame = frame
        self.combobox = ttk.Combobox(root, values=["All", "PSP", "PSX", "PS2", "PS3"])
        self.combobox.place(x=x, y=y)
        self.combobox.current(0)
        self.combobox.config(width='4', state="readonly")

    def get_box(self):
        return self.combobox


