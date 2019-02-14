from tkinter import *
from tkFont import Font

class Main_UI():


	def __init__(self, main):

		# canvas for image
		self.canvas = Canvas(main, width=main_width, height=main_height, borderwidth =0, highlightthickness=0)
		self.canvas.grid(row=0, column=0)

		# images
		self.my_images = []
		self.my_images.append(PhotoImage(file='gui_background_1920_1080_merged.gif'))
		self.my_images.append(PhotoImage(file='gui_background_1920_1080_dark.gif'))
		self.my_images.append(PhotoImage(file='gui_background_1920_1080.gif'))
		self.my_images.append(PhotoImage(file='ps3_blue_waves_1920_1080.gif'))
		self.my_images.append(PhotoImage(file='ps3_blue_waves_2_1920_1080.gif'))
		self.my_images.append(PhotoImage(file='ps3_blue_waves_3_1920_1080.gif'))
		self.my_image_number = 0

		# set first image on canvas
		self.image_on_canvas = self.canvas.create_image(0, 0, anchor = NW, image = self.my_images[self.my_image_number])
		self.init_main_window_buttons(main)
		self.init_param_sfo_labels(main)

	def init_param_sfo_labels(self, main):
		# Constants
		dark_side_width 		= main_width-30
		dark_side_height 		= main_height-30
		dark_side_panel_x_y		= [686, 19]

		dark_side_text_space	= 20
		dark_side_padding 		= 20

		text_title_id 	= 'TITLE ID'
		text_title		= 'TITLE'
		text_iso_path	= 'ISO PATH'

		height_of_text 			= Font(font='Helvetica').metrics('linespace')
		width_of_title_id_text 	= Font(size=15, family='Helvetica').measure(text_title_id) +1
		width_of_title_text 	= Font(size=15, family='Helvetica').measure(text_title) +1
		width_of_iso_path_text 	= Font(size=15, family='Helvetica').measure(text_iso_path) +1
		
		print('DEBUG height_of_text: ' 			+ str(height_of_text))
		print('DEBUG width_of_title_id_text: ' 	+ str(width_of_title_id_text))
		print('DEBUG width_of_title_text: ' 	+ str(width_of_title_text))
		print('DEBUG width_of_iso_path_text: ' 	+ str(width_of_iso_path_text))

		title_id_text_x_pos		= dark_side_panel_x_y[0] + 1*dark_side_padding + width_of_title_id_text/2
		title_id_text_y_pos 	= dark_side_panel_x_y[1] + 1*dark_side_padding + dark_side_padding

		title_text_x_pos		= dark_side_panel_x_y[0] + 1*dark_side_padding + width_of_title_text/2
		title_text_y_pos 		= title_id_text_y_pos + height_of_text + dark_side_padding

		iso_path_text_x_pos		= dark_side_panel_x_y[0] + 1*dark_side_padding + width_of_iso_path_text/2
		iso_path_text_y_pos 	= title_text_y_pos + height_of_text + dark_side_padding

		self.title_id_text_id 	= self.canvas.create_text(title_id_text_x_pos, title_id_text_y_pos, 	text=text_title_id,	fill="White", font=("Helvetica", 15))
		self.title_text_id 		= self.canvas.create_text(title_text_x_pos, 	title_text_y_pos, 		text=text_title , 	fill="White", font=("Helvetica", 15))
		self.iso_path_text_id 	= self.canvas.create_text(iso_path_text_x_pos, iso_path_text_y_pos,	text=text_iso_path,	fill="White", font=("Helvetica", 15))

		e1 = Entry(main)
		e2 = Entry(main)
		e3 = Entry(main)
		e1.place(x=5*dark_side_padding + width_of_title_id_text + dark_side_panel_x_y[0], 	y=title_id_text_y_pos	-15)
		e2.place(x=5*dark_side_padding + width_of_title_id_text	+ dark_side_panel_x_y[0], 	y=title_text_y_pos		-15)
		e3.place(x=5*dark_side_padding + width_of_title_id_text + dark_side_panel_x_y[0], 	y=iso_path_text_y_pos	-15)

	def init_main_window_buttons(self, main):

		# button to quit
		self.quit_button = Button(main, text="Quit", command=main.quit, bd=1, bg="#FBFCFB")
		self.quit_button.place(x=0, y=0)
		self.quit_button.config(height=1, width=3)

		# button to change image
		self.change_button = Button(main, text="Change", command=self.on_change_button, bd=1, bg="#FBFCFB")
		self.change_button.place(x=45, y=0)

	def on_change_button(self):

		# next image
		self.my_image_number += 1

		# return to first image
		if self.my_image_number == len(self.my_images):
			self.my_image_number = 0

		# change image
		self.canvas.itemconfig(self.image_on_canvas, image = self.my_images[self.my_image_number])


main_width = 1920
main_height = 1080



main_window = Tk()
# changing the title of our master widget
main_window.title('webMAN Classics Maker UI')
# icon upper left corner
main_window.iconbitmap(r'../../images/webman.ico')

Main_UI(main_window)
main_window.mainloop()