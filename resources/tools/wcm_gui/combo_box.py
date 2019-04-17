try:
    # Python2
    import Tkinter as tk
    import ttk
except ImportError:
    # Python3
    import tkinter as tk
    import ttk



class ComboBox:

    def make_combo_box(self, root, x, y):
        combobox = ttk.Combobox(root, values=["All", "PSP", "PSX", "PS2", "PS3"])
        combobox.place(x=x, y=y)
        combobox.current(3)

        return combobox

