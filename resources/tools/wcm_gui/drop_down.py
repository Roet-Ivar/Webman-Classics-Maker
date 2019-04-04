try:
    # Python2
    import Tkinter as tk
except ImportError:
    # Python3
    import tkinter as tk



class ComboBox:


    def __init__(self, root):
        self.var = tk.StringVar(root)

    def make_combo_box(self, root, x, y):
        # initial value
        self.var.set('PS2')

        choices = ['PSP', 'PSX', 'PS2', 'PS3']
        option = tk.OptionMenu(root, self.var, *choices)
        option.place(x=x, y=y)


# root = tk.Tk()
# cb = ComboBox()
# cb.make_combo_box(root, 10, 10)
#
#
# root.mainloop()