from tkinter import ttk


class DriveDropdown:
    def __init__(self, canvas):
        # disabled PSP for now
        x = 1100
        y = 247

        self.combobox = ttk.Combobox(canvas, values=["ALL", "HDD0", "USB(*)", "USB000", "USB001", "USB002", "USB003"],
                                     name="drive_dropdown")
        self.combobox.place(x=x, y=y)
        self.combobox.current(0)
        self.combobox.config(width=7, state="readonly")

    def get_dropdown(self):
        return self.combobox


class PlatformDropdown:
    def __init__(self, canvas):
        x = 1100 + 70
        y = 247

        self.combobox = ttk.Combobox(canvas, values=["ALL", "PSPISO", "PSXISO", "PS2ISO", "PS3ISO", 'NTFS', "GAMES"],
                                     name="platform_dropdown")
        self.combobox.place(x=x, y=y)
        self.combobox.current(0)
        self.combobox.config(width=7, state="readonly")

    def get_dropdown(self):
        return self.combobox


