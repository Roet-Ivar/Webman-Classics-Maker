#!/usr/bin/python

# Inspiration, PS2 Classic GUI: https://i.imgur.com/FcV6uN6.png

from tkinter import *
from tkinter import ttk
from decimal import Decimal

class App(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_grid()
		self.init_main_window_buttons()

		
	def init_grid(self):
		photo1  = PhotoImage(file='../../images/gui_background_1000_600.gif')
		photo2  = PhotoImage(file='../../images/gui_background_1000_600_dark.gif')
		
		left_side_weigth = 8
		right_side_weigth = 9
		weigth_ratio = round(1+(Decimal(left_side_weigth)/Decimal(right_side_weigth)), 2)
		print('weigth_ratio: ' + str(weigth_ratio))

		
		top_row_heigth = 0
		bottom_row_heigth = 35
		
		main_label = Label(root, image=photo1)
		main_label.photo = photo1
		
		
		frame_top_row    		= Frame(root, width=main_window_width, height=top_row_heigth, bg="")
		frame_bottom_row   		= Frame(root, width=main_window_width, height=bottom_row_heigth, bg="")

		frame_middle_row 		= Frame(root, bg="")
		frame_middle_row_left	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-top_row_heigth, bg="#000fff000")
		frame_middle_row_right	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-top_row_heigth, bg="#000ffffff")



		root.grid_rowconfigure(1,weight=1)
		root.grid_columnconfigure(0,weight=1)


		frame_top_row.grid(row=0,sticky="ew")
		frame_bottom_row.grid(row=2,sticky="ew")
		frame_middle_row.grid(row=1,sticky="ew")

		frame_middle_row_left.grid(row=0, column=0,sticky="w", in_=frame_middle_row)
		frame_middle_row_right.grid(row=0, column=1,sticky="e", in_=frame_middle_row)

		frame_middle_row.grid_columnconfigure(0,weight=left_side_weigth)
		frame_middle_row.grid_columnconfigure(1,weight=right_side_weigth)
		frame_top_row.grid_columnconfigure(0,weight=1)
		
		left_label = Label(frame_middle_row_left, image=photo1)
		left_label.photo = photo1
		
		right_label = Label(frame_middle_row_right, image=photo2)
		right_label.photo = photo2
		
		
		main_label.place(x=0, y=0)
		left_label.place(x=0, y=-top_row_heigth)
		right_label.place(x=-(main_window_width/weigth_ratio), y=-top_row_heigth)
		


	def init_main_window_buttons(self):
		# creating a button instance
		fileMenuButton = Button(root, text = "File", anchor = W)
		quitButton = Button(root, text = "Quit", command = root.quit, anchor = W)

		# placing the button on my window
		fileMenuButton.place(x=0, y=2)
		quitButton.place(x=35, y=2)


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