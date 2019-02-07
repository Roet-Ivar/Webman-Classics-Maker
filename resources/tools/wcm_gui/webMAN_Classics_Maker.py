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
		bg_light  = PhotoImage(file='../../images/gui_background_1280_720.gif')
		bg_dark  = PhotoImage(file='../../images/gui_background_1280_720_dark.gif')
		
		# Constants
		top_row_heigth = 35
		bottom_row_heigth = 35
		
		left_side_weigth = 8
		right_side_weigth = 9
		weigth_ratio = round(1+(Decimal(left_side_weigth)/Decimal(right_side_weigth)), 2)
		
		frame_top_row    		= Frame(root, width=main_window_width, height=top_row_heigth, bg="")
		frame_bottom_row   		= Frame(root, width=main_window_width, height=bottom_row_heigth, bg="")
		frame_middle_row 		= Frame(root, bg="")
		frame_middle_row_left	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-top_row_heigth, bg="")
		frame_middle_row_right	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-top_row_heigth, bg="")
		
		
		frame_top_row.grid(row=0,sticky="ew")
		frame_bottom_row.grid(row=2,sticky="ew")
		frame_middle_row.grid(row=1,sticky="ew")
		frame_middle_row_left.grid(row=0, column=0,sticky="w", in_=frame_middle_row)
		frame_middle_row_right.grid(row=0, column=1,sticky="e", in_=frame_middle_row)

		
		frame_middle_row.grid_columnconfigure(0,weight=left_side_weigth)
		frame_middle_row.grid_columnconfigure(1,weight=right_side_weigth)
		frame_top_row.grid_columnconfigure(0,weight=1)
		root.grid_rowconfigure(1,weight=1)
		root.grid_columnconfigure(0,weight=1)

		top_label 			= Label(frame_top_row, image=bg_light)
		bottom_label 		= Label(frame_bottom_row, image=bg_light)
		left_label 			= Label(frame_middle_row_left, image=bg_light)
		right_label 		= Label(frame_middle_row_right, image=bg_dark)
		
		bottom_label.photo 	= bg_light
		top_label.photo 	= bg_light
		left_label.photo 	= bg_light
		right_label.photo	= bg_dark
		
		# Label placements (-5 to hide left side border)
		top_label.place(x=-5, y=0 -5)
		bottom_label.place(x=-5, y=-main_window_height+top_row_heigth -5)
		left_label.place(x=-5, y=-top_row_heigth -5)
		right_label.place(x=-(main_window_width/weigth_ratio)-5, y=-top_row_heigth -5)
		
		
		# Label(frame_middle_row_left, text="Last Name").grid(row=1)

	def init_main_window_buttons(self):
		# creating a button instance
		# bone white #FFF3E8
		fileMenuButton = Button(root, text = "File", anchor = W, relief=FLAT, bg="#FBFCFB")
		quitButton = Button(root, text = "Quit", command = root.quit, anchor = W, relief=FLAT, bg="#FBFCFB")

		# placing the button on my window
		fileMenuButton.place(x=0, y=2)
		quitButton.place(x=35, y=2)
		


root = Tk()

# Size of the window
main_window_width=1270
main_window_height=715

# changing the title of our master widget
root.title('webMAN Classics Maker UI alpha 1')

# icon upper left corner
root.iconbitmap(r'../../images/webman.ico')

root.geometry('{}x{}'.format((main_window_width), str(main_window_height)) )
root.resizable(width=FALSE, height=FALSE)



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