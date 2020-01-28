try:
    # Python2
    import Tkinter as tk
    import ttk
except ImportError:
    # Python3
    import tkinter as tk
    import ttk



class ComboBox:

    def make_combo_box(self, root, frame, x, y):
        # disabled PSP for now
        self.root = root
        self.frame = frame
        self.combobox = ttk.Combobox(root, values=["PSP", "PSX", "PS2", "PS3", "All"])
        self.combobox.place(x=x, y=y)
        self.combobox.current(3)

        frame.bind('<Enter>', self._bound_to_mousewheel)
        frame.bind('<Leave>', self._unbound_to_mousewheel)

        return self.combobox

    def _bound_to_mousewheel(self, event):
        self.frame.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self.frame.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self.frame.yview_scroll(int(-1*(event.delta/30)), "units")


