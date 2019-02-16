import os
import json
from Tkinter import *
from tkFont import Font


class Main():


	def __init__(self, main):
		self.vcmd = main.register(self.validate)
		self.maxlength = 8

		self.entry_field_title_id = None
		self.entry_field_title = None
		self.entry_field_iso_path = None

		# canvas for image
		self.canvas = Canvas(main, width=canvas_width, height=canvas_height, borderwidth =0, highlightthickness=0)
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
		text_title_id 	= 'TITLE ID'
		text_title		= 'TITLE'
		text_iso_path	= 'ISO PATH'

		height_of_text 			= Font(font='Helvetica').metrics('linespace')
		width_of_title_id_text 	= Font(size=15, family='Helvetica').measure(text_title_id) +1
		width_of_title_text 	= Font(size=15, family='Helvetica').measure(text_title) +1
		width_of_iso_path_text 	= Font(size=15, family='Helvetica').measure(text_iso_path) +1

		print('DEBUG height_of_text: ' 			+ str(height_of_text))
		print('DEBUG width_of_title_id_text: '	+ str(width_of_title_id_text))
		print('DEBUG width_of_title_text: '		+ str(width_of_title_text))
		print('DEBUG width_of_iso_path_text: '	+ str(width_of_iso_path_text))


		# Coordinates
		main_offset_x_pos	= 950
		main_offset_y_pos	= 50

		dark_side_padding	= 20
		text_box_spacing	= 4*dark_side_padding

		title_id_text_x_pos	= main_offset_x_pos + width_of_title_id_text/2
		title_id_text_y_pos = main_offset_y_pos + height_of_text/2

		title_text_x_pos	= main_offset_x_pos + width_of_title_text/2
		title_text_y_pos	= dark_side_padding + title_id_text_y_pos + height_of_text

		iso_path_text_x_pos	= main_offset_x_pos + width_of_iso_path_text/2
		iso_path_text_y_pos	= dark_side_padding + title_text_y_pos + height_of_text


		# Placements
		self.title_id_text_id 	= self.canvas.create_text(title_id_text_x_pos,	title_id_text_y_pos, 	text=text_title_id,	fill="White", font=("Helvetica", 15))
		self.title_text_id 		= self.canvas.create_text(title_text_x_pos,		title_text_y_pos, 		text=text_title , 	fill="White", font=("Helvetica", 15))
		self.iso_path_text_id 	= self.canvas.create_text(iso_path_text_x_pos,	iso_path_text_y_pos,	text=text_iso_path,	fill="White", font=("Helvetica", 15))

		self.entry_field_title_id 	= Entry(main, validate='key', validatecommand=(self.vcmd, '%P'))
		self.entry_field_title 		= Entry(main)
		self.entry_field_iso_path 	= Entry(main)

		self.entry_field_title_id.place(	x=text_box_spacing 	+  iso_path_text_x_pos, y=title_id_text_y_pos 	-height_of_text/2, width=200)
		self.entry_field_title.place(		x=text_box_spacing 	+  iso_path_text_x_pos, y=title_text_y_pos		-height_of_text/2, width=200)
		self.entry_field_iso_path.place(	x=text_box_spacing 	+  iso_path_text_x_pos, y=iso_path_text_y_pos 	-height_of_text/2, width=200)

		# dark side save-button
		self.save_button = Button(main, text="Save", command=self.on_save_button, bd=1, bg="#FBFCFB")
		self.save_button.place(x=text_box_spacing 	+  iso_path_text_x_pos + 200, y=720 - 30)

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

	def on_save_button(self):
		# do stuff
		print('\nDEBUG SAVE BUTTON PRESSED')
		print('DEBUG entry_field_title_id: ' 	+ self.entry_field_title_id.get())
		print('DEBUG entry_field_id: ' 			+ self.entry_field_title.get())
		print('DEBUG entry_field_iso_path: ' 	+ self.entry_field_iso_path.get())

		self.save_pkg_info_to_json()

	def save_pkg_info_to_json(self):
		with open('../util_resources/params.json.BAK') as f:
			json_data = json.load(f)

		try:
			title_id = self.entry_field_title_id.get().upper()
			if len(title_id) > self.maxlength:
				title_id = title_id[0:self.maxlength]
				self.entry_field_title_id.delete(0, END)
				self.entry_field_title_id.insert(0, title_id)
				print('new val: ' + self.entry_field_title_id.get())

			json_data['title']=str(self.entry_field_title.get())
			json_data['title_id']=title_id
			json_data['content_id']='UP0001-'+ str(self.entry_field_title_id.get()) + '_00-0000000000000000'
			json_data['iso_filepath']=str(self.entry_field_iso_path.get())

			newFile = open("../util_generated_files/webman_classics_pkg.json", "w")
			json_text = json.dumps(json_data, indent=4, separators=(",", ":"))
			newFile.write(json_text)

		except ValueError:
			print('File write error/PKGLAUNCH not found/titel_id not a string')

	def validate(self, P):
		if len(P) > self.maxlength:
			print('DEBUG Title ID longer than 8 characters!')
			main_window.after_idle(lambda: self.entry_field_title_id.config(validate='key'))
			return None  # new value too long
		else:
			print('DEBUG Title ID: ' + P)
			return True


canvas_width = 1920
canvas_height = 1080

main_window_width = 1350
main_window_height = 720

main_window = Tk()
# changing the title of our master widget
main_window.title('webMAN Classics Maker UI')
# icon upper left corner
main_window.iconbitmap(r'../../images/webman.ico')

main_window.geometry(str(main_window_width) + 'x' + str(main_window_height))
Main(main_window)

main_window.mainloop()
