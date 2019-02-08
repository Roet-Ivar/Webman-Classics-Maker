#!/usr/bin/python

# Inspiration, PS2 Classic GUI: https://i.imgur.com/FcV6uN6.png

from tkinter import *
import ttk

class App(Frame):

	def __init__(self, master=None):
		Frame.__init__(self, master)
		self.master = master
		self.init_main_window()
		self.init_main_window_buttons()
		self.init_treeview()

	#Creation of init_window
	def init_main_window(self):

		# changing the title of our master widget      
		self.master.title('webMAN Classics Maker 1.1.3 alfa')

		# icon upper left corner
		self.master.iconbitmap(r'../../images/webman.ico')

		# filling the backround image
		photo  = PhotoImage(file='../../images/gui_background_1000_600.gif')
		w = Label(self, image=photo)
		w.place(x=0, y=0)
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
		
	def init_treeview(self):
		tree = ttk.Treeview(root)
		tree["columns"]=("one","two")
		tree.column("one", width=100 )
		tree.column("two", width=100)
		# tree.heading("one", text="coulmn A")
		# tree.heading("two", text="column B")
		
		# tree.insert("" , 0,    text="Line 1", values=("1A","1b"))

		# id2 = tree.insert("", 1, "dir2", text="Dir 2")
		# tree.insert(id2, "end", "dir 2", text="sub dir 2", values=("2A","2B"))
		
		#alternatively:
		# tree.insert("", 3, "dir3", text="Dir 3")
		# tree.insert("dir3", 3, text=" sub dir 3",values=("3A"," 3B"))

		tree.place(x=100, y=400)
	

root = Tk()

# Size of the window
main_window_width=1000
main_window_height=600
root.geometry(str(main_window_width) + 'x' + str(main_window_height)) 

app = App(root)
root.mainloop()