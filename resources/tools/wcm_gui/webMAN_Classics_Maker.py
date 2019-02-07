#!/usr/bin/python

# Inspiration, PS2 Classic GUI: https://i.imgur.com/FcV6uN6.png

from tkinter import *

class App:
	def __init__(self,master):
		frame = Frame(master)
		master.title('webMAN Classics Maker 1.1.3 alfa')
		master.iconbitmap(r'../../images/webman.ico') # icon upper left corner
		master.geometry('1000x600') # Size of the window
		frame.pack()
		photo  = PhotoImage(file='../../images/gui_background_1000_600.gif')
		w = Label (master, image=photo)
		w.place(x=10, y=10, relwidth=1, relheight=1)
		w.photo = photo
		w.pack()


root = Tk()
app = App(root)
root.mainloop()