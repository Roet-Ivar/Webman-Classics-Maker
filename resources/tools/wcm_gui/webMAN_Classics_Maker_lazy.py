
from tkinter import *

#----------------------------------------------------------------------

class MainWindow():

	#----------------

	def __init__(self, main):

		self.button = Button(main, text = "Quit", command = root.quit, anchor = W, bg="#FBFCFB")
		self.button.grid(row=0, column=0)
	
		# canvas for image
		self.canvas = Canvas(main, width=main_width, height=main_heigth, borderwidth =0, highlightthickness=0)
		self.canvas.grid(row=1, column=0)

		# images
		self.my_images = []
		self.my_images.append(PhotoImage(file='gui_background_1280_720_merged.gif'))
		self.my_images.append(PhotoImage(file='gui_background_1280_720_dark.gif'))
		self.my_images.append(PhotoImage(file='gui_background_1280_720.gif'))
		self.my_image_number = 0

		# set first image on canvas
		self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images[self.my_image_number])

		# button to change image
		self.button = Button(main, text="Change", command=self.onButton)
		self.button.grid(row=2, column=0)


	

	#----------------

	def onButton(self):

		# next image
		self.my_image_number += 1

		# return to first image
		if self.my_image_number == len(self.my_images):
			self.my_image_number = 0

		# change image
		self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])
		

	def init_main_window_buttons(self):
		# creating a button instance
		# bone white #FFF3E8
		fileMenuButton = Button(root, text = "File", anchor = W, relief=FLAT, bg="#FBFCFB")
		quitButton = Button(root, text = "Quit", command = root.quit, anchor = W, relief=FLAT, bg="#FBFCFB")

		# placing the button on my window
		fileMenuButton.place(x=0, y=2)
		quitButton.place(x=35, y=2)

#----------------------------------------------------------------------

main_width=1280
main_heigth=720

root = Tk()

# changing the title of our master widget
root.title('webMAN Classics Maker UI')

# icon upper left corner
root.iconbitmap(r'../../images/webman.ico')


MainWindow(root)
root.mainloop()