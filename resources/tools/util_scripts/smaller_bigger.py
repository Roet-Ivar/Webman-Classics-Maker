from __future__ import print_function
import Tkinter as tk


class My_App(tk.Frame):

    def __init__(self, parent):
        tk.Frame.__init__(self, parent)

        # we need to set parent as a class attribute for later use
        self.parent = parent
        button1 = tk.Button(self.parent, text="Make window larger!", command = self.make_window_bigger)
        button1.pack()

        button2 = tk.Button(self.parent, text="Make window Smaller!", command = self.make_window_smaller)
        button2.pack()

    def make_window_bigger(self):
        x = self.parent.winfo_height() + 10
        y = self.parent.winfo_width() + 10
        self.parent.geometry('{}x{}'.format(y, x))

    def make_window_smaller(self):
        x = self.parent.winfo_height() - 10
        y = self.parent.winfo_width() - 10
        self.parent.geometry('{}x{}'.format(y, x))

root = tk.Tk()
My_App(root)
root.mainloop()