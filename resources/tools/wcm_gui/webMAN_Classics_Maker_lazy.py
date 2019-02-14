from tkinter import *
from tkinter import font

class Main_UI():


	def __init__(self, main):


	
		# canvas for image
		self.canvas = Canvas(main, width=main_width, height=main_height, borderwidth =0, highlightthickness=0)
		self.canvas.grid(row=0, column=0)

		# images
		self.my_images = []
		self.my_images.append(PhotoImage(file='gui_background_1280_720_merged.gif'))
		self.my_images.append(PhotoImage(file='gui_background_1280_720_dark.gif'))
		self.my_images.append(PhotoImage(file='gui_background_1280_720.gif'))
		self.my_image_number = 0

		# set first image on canvas
		self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images[self.my_image_number])
		self.init_main_window_buttons(main)
		self.init_param_sfo_labels(main)

	def init_param_sfo_labels(self, main):

		text_title_id 	= 'Title ID'
		text_title		= 'Title'
		text_iso_path	= 'ISO path'

		height_of_text 			= font.Font(font='TkDefaultFont').metrics('linespace')
		width_of_title_id_text 	= font.Font(size=9, family='TkDefaultFont').measure(text_title_id)
		width_of_title_text 	= font.Font(size=9, family='TkDefaultFont').measure(text_title)
		width_of_iso_path_text 	= font.Font(size=9, family='TkDefaultFont').measure(text_iso_path)

		title_id_text_x			= dark_side_panel_x_y[0] + dark_side_padding + width_of_title_id_text / 2
		title_id_text_y 		= dark_side_panel_x_y[1] + 1 * dark_side_padding + height_of_text / 2

		title_text_x			= dark_side_panel_x_y[0] + dark_side_padding + width_of_title_text / 2
		title_text_y 			= dark_side_panel_x_y[1] + 2 * dark_side_padding + height_of_text / 2

		iso_path_text_x			= dark_side_panel_x_y[0] + dark_side_padding + width_of_iso_path_text / 2
		iso_path_text_y 		= dark_side_panel_x_y[1] + 3 * dark_side_padding + height_of_text / 2

		self.title_id_text_id = self.canvas.create_text(title_id_text_x, title_id_text_y, text=text_title_id, fill="White")
		self.title_text_id = self.canvas.create_text(title_text_x, title_text_y, text=text_title, fill="White")
		self.iso_path_text_id = self.canvas.create_text(iso_path_text_x, iso_path_text_y, text=text_iso_path, fill="White")
		# bounds = self.canvas.bbox(self.title_id_text_id)
		# print('bounds width: ' + str(bounds[2] - bounds[0]))
		# print('bounds height: ' + str(bounds[3] - bounds[1]))

		e1 = Entry(main)
		e1.grid(row=0, column=0)
		e1.place(x=dark_side_padding + width_of_title_id_text + dark_side_panel_x_y[0] + dark_side_padding, y=dark_side_padding + dark_side_panel_x_y[1])

	def init_main_window_buttons(self, main):

		# button to quit
		self.quit_button = Button(main, text="Quit", command=main.quit, bd=1, bg="#FBFCFB")
		self.quit_button.place(x=0, y=0)
		self.quit_button.config(height=1, width=3)

		# button to change image
		self.change_button = Button(main, text="Change", command=self.on_change_button, bd=1, bg="#FBFCFB")
		self.change_button.place(x=30, y=0)

	def on_change_button(self):

		# next image
		self.my_image_number += 1

		# return to first image
		if self.my_image_number == len(self.my_images):
			self.my_image_number = 0

		# change image
		self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])


main_width = 1280
main_height = 720

dark_side_width = main_width-30
dark_side_height = main_height-30
dark_side_panel_x_y = [686, 19]

dark_side_text_space = 20
dark_side_padding = 20

main_window = Tk()
# changing the title of our master widget
main_window.title('webMAN Classics Maker UI')
# icon upper left corner
main_window.iconbitmap(r'../../images/webman.ico')

Main_UI(main_window)
main_window.mainloop()