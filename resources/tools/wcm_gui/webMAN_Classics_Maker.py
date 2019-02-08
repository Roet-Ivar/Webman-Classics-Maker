#!/usr/bin/python

# Inspiration, PS2 Classic GUI: https://i.imgur.com/FcV6uN6.png

from tkinter import *
from tkinter import ttk

class App(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		# self.init_main_window()
		self.init_grid()
		self.init_main_window_buttons()

		
	def init_grid(self):
		frame_top    			= Frame(root, width=main_window_width, height=50, bg="")
		frame_bottom   			= Frame(root, width=main_window_width, height=50, bg="")

		frame_middle_row 		= Frame(root, bg="")
		frame_middle_row_left	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-50, bg="#000fff000")
		frame_middle_row_right	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-50, bg="#000ffffff")


		root.grid_rowconfigure(1,weight=1)
		root.grid_columnconfigure(0,weight=1)


		frame_top.grid(row=0,sticky="ew")
		frame_bottom.grid(row=2,sticky="ew")
		frame_middle_row.grid(row=1,sticky="ew")

		frame_middle_row_left.grid(row=0, column=0,sticky="w", in_=frame_middle_row)
		frame_middle_row_right.grid(row=0, column=1,sticky="e", in_=frame_middle_row)


		frame_middle_row.grid_columnconfigure(0,weight=2)
		frame_middle_row.grid_columnconfigure(1,weight=1)
		frame_top.grid_columnconfigure(0,weight=1)
		
	#Creation of init_window
	def init_main_window(self):
		# top_frame = Frame(self.master, bg='cyan', width=450, height=50, pady=3).grid(row=0, columnspan=3)
		# changing the title of our master widget
		self.master.title('webMAN Classics Maker UI alpha 1')

		# icon upper left corner
		self.master.iconbitmap(r'../../images/webman.ico')

		# filling the background image
		photo  = PhotoImage(file='../../images/gui_background_1000_600.gif')
		w = Label(self, image=photo)
		w.place(x=-5, y=-5)
		w.photo = photo

		# allowing the widget to take the full space of the root window
		self.pack(fill=BOTH, expand=1)


	def init_main_window_buttons(self):
		# creating a button instance
		quitButton = Button(root, text = "Quit", command = root.quit, anchor = W)

		# placing the button on my window
		quitButton.place(x=5, y=5)

		# creating a button instance
		makeButton = Button(root, text = "Make", anchor = W)

		# placing the button on my window
		makeButton.place(x=55, y=5)


root = Tk()

# Size of the window
main_window_width=1000
main_window_height=600

# changing the title of our master widget
root.title('webMAN Classics Maker UI alpha 1')

# icon upper left corner
root.iconbitmap(r'../../images/webman.ico')

root.geometry('{}x{}'.format((main_window_width), str(main_window_height)) )
root.resizable(width=FALSE, height=FALSE)


app = App(root)
root.mainloop()