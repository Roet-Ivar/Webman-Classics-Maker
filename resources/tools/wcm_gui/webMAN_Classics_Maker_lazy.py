import json
import sys

if sys.version_info[0] < 3:
	from Tkinter import *
	from tkFont import Font
else:
	from tkinter import *
	from tkinter.font import Font


class Main():


	def __init__(self, main):
		self.vcmd = main.register(self.validate)
		self.vcmd2 = main.register(self.validate)
		self.maxlength = 8

		self.entry_field_title_id 	= None
		self.entry_field_title 		= None
		self.entry_field_iso_path 	= None

		# canvas for image
		self.canvas = Canvas(main, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0)
		self.canvas.grid(row=0, column=0)

		# images
		self.logos = []
		self.logos.append(PhotoImage(file='logo_PSP.gif'))
		self.logos.append(PhotoImage(file='logo_PSX.gif'))
		self.logos.append(PhotoImage(file='logo_PS2.gif'))
		self.logos.append(PhotoImage(file='logo_PS3.gif'))


		self.wallpapers = []
		self.wallpapers.append(PhotoImage(file='gui_background_1920_1080_merged.gif'))
		self.wallpapers.append(PhotoImage(file='gui_background_1920_1080_dark.gif'))
		self.wallpapers.append(PhotoImage(file='gui_background_1920_1080.gif'))
		self.wallpapers.append(PhotoImage(file='ps3_blue_waves_1920_1080.gif'))
		self.wallpapers.append(PhotoImage(file='ps3_blue_waves_2_1920_1080.gif'))
		self.wallpapers.append(PhotoImage(file='ps3_blue_waves_3_1920_1080.gif'))


		# set first image on canvas
		self.my_image_number = 0
		self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.wallpapers[self.my_image_number])
		self.init_main_window_buttons(main)
		self.init_param_sfo_labels(main)

	def init_param_sfo_labels(self, main):
		# Constants
		text_title_id 			= 'TITLE ID'
		text_title				= 'TITLE'
		text_filename			= 'FILENAME'
		text_iso_path			= 'ISO PATH'

		height_of_text 			= Font(font='Helvetica').metrics('linespace')
		width_of_title_id_text 	= Font(size=15, family='Helvetica').measure(text_title_id)
		width_of_title_text 	= Font(size=15, family='Helvetica').measure(text_title)
		width_of_filename_text	= Font(size=15, family='Helvetica').measure(text_filename)
		width_of_iso_path_text 	= Font(size=15, family='Helvetica').measure(text_iso_path)

		print('DEBUG height_of_text: ' 			+ str(height_of_text))
		print('DEBUG width_of_title_id_text: '	+ str(width_of_title_id_text))
		print('DEBUG width_of_title_text: '		+ str(width_of_title_text))
		print('DEBUG width_of_iso_path_text: '	+ str(width_of_iso_path_text))


		# coordinates
		main_offset_x_pos		= 950
		main_offset_y_pos		= 100

		# distances
		dark_side_padding		= 20
		text_box_spacing		= 4*dark_side_padding


		title_id_text_x_pos		= main_offset_x_pos + width_of_title_id_text/2
		title_id_text_y_pos 	= main_offset_y_pos + height_of_text/2

		title_text_x_pos		= main_offset_x_pos + width_of_title_text/2
		title_text_y_pos		= dark_side_padding + title_id_text_y_pos + height_of_text

		filename_text_x_pos		= main_offset_x_pos + width_of_filename_text/2
		filename_text_y_pos		= dark_side_padding + title_text_y_pos + height_of_text

		iso_path_text_x_pos		= main_offset_x_pos + width_of_iso_path_text/2
		iso_path_text_y_pos		= dark_side_padding + filename_text_y_pos + height_of_text


		# Placements
		self.title_id_text_id 	= self.canvas.create_text(title_id_text_x_pos,	title_id_text_y_pos,	text=text_title_id,	fill="White", font=("Helvetica", 15))
		self.title_text_id 		= self.canvas.create_text(title_text_x_pos,		title_text_y_pos, 		text=text_title, 	fill="White", font=("Helvetica", 15))
		self.title_filename 	= self.canvas.create_text(filename_text_x_pos,	filename_text_y_pos, 	text=text_filename,	fill="White", font=("Helvetica", 15))
		self.iso_path_text_id 	= self.canvas.create_text(iso_path_text_x_pos,	iso_path_text_y_pos,	text=text_iso_path,	fill="White", font=("Helvetica", 15))

		self.entry_field_title_id	= Entry(main, validate='key', validatecommand=(self.vcmd, '%P'))
		self.entry_field_title		= Entry(main)
		self.entry_field_filename 	= Entry(main)
		self.entry_field_iso_path	= Entry(main) #, state='disabled')

		self.entry_field_title_id.place(x=text_box_spacing + iso_path_text_x_pos, y=title_id_text_y_pos	-height_of_text/3, width=200)
		self.entry_field_title.place(	x=text_box_spacing + iso_path_text_x_pos, y=title_text_y_pos	-height_of_text/3, width=200)
		self.entry_field_filename.place(x=text_box_spacing + iso_path_text_x_pos, y=filename_text_y_pos -height_of_text/3, width=200)
		self.entry_field_iso_path.place(x=text_box_spacing + iso_path_text_x_pos, y=iso_path_text_y_pos -height_of_text/3, width=200)

		############################################
		self.generateOnChange(self.entry_field_filename)
		self.entry_field_filename.bind('<<Change>>', self.onEntryChanged)
		############################################

		# system choice buttons
		self.selection_drive_list	= ['hdd0', 'dev_usb00x']			# usb port 'x' should be selected through a list
		self.selection_system_list	= ['PSP', 'PSX', 'PS2', 'PS3']
		self.drive_path 			= self.selection_drive_list[0] 		# drive should be toggled by buttons

		self.button_PSP = Button(main, image=self.logos[0], bd=1, command=lambda: self.on_system_choice_button(self.drive_path, self.selection_system_list[0], ''))
		self.button_PSX = Button(main, image=self.logos[1], bd=1, command=lambda: self.on_system_choice_button(self.drive_path, self.selection_system_list[1], ''))
		self.button_PS2 = Button(main, image=self.logos[2], bd=1, command=lambda: self.on_system_choice_button(self.drive_path, self.selection_system_list[2], ''))
		self.button_PS3 = Button(main, image=self.logos[3], bd=1, command=lambda: self.on_system_choice_button(self.drive_path, self.selection_system_list[3], ''))

		self.button_PSP.place(x=main_offset_x_pos + 0 * 29, y=40)
		self.button_PSX.place(x=main_offset_x_pos + 3 * 29, y=40)
		self.button_PS2.place(x=main_offset_x_pos + 6 * 29, y=40)
		self.button_PS3.place(x=main_offset_x_pos + 9 * 29, y=40)


		# dark side save-button
		self.save_button = Button(main, text="Save", command=self.on_save_button, bd=1, bg="#FBFCFB")
		self.save_button.place(x=text_box_spacing 	+  iso_path_text_x_pos + 168, y=iso_path_text_y_pos + 20)

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
		if self.my_image_number == len(self.wallpapers):
			self.my_image_number = 0

		# change image
		self.canvas.itemconfig(self.image_on_canvas, image = self.wallpapers[self.my_image_number])

	def on_system_choice_button(self, drive_choice, system_choice, filename):

		change_drive 	= False
		change_system 	= False
		change_filname 	= False

		current_iso_path = self.entry_field_iso_path.get()
		# print('DEBUG entry_field_iso_path.get(): ' + current_iso_path)
		# print('DEBUG drive_path: ' + drive_path)
		# print('DEBUG system_string: ' + system_string)
		if current_iso_path == '':
			new_system_path = '/' + drive_choice + '/' + system_choice + '/'
			print('new system_path: ' + new_system_path)
			self.entry_field_iso_path.delete(0, END)
			self.entry_field_iso_path.insert(0, new_system_path)
			return


		if drive_choice not in current_iso_path:
			change_drive = True
		if system_choice not in current_iso_path:
			change_system = True

		# if change_drive == False and change_system == False:
		# 	return


		if change_drive:
			# Check if drive path has been initialized
			for drive in self.selection_drive_list:
				if drive in current_iso_path:
					print('DEBUG Current drive path is: ' + drive + ', changing to ' + drive_choice)

		if change_system:
			# Check if system path has been initialized
			for drive in self.selection_drive_list:
				if drive in current_iso_path:
					print('DEBUG Current drive path is: ' + drive + ', changing to ' + drive_choice)
			print('DEBUG Drive path has not been initialized')
			print('Adding ' + drive_choice + ' to the path.')
			# return


	def on_save_button(self):
		# do stuff

		self.save_pkg_info_to_json()

	def save_pkg_info_to_json(self):
		with open('../util_resources/params.json.BAK') as f:
			json_data = json.load(f)

		try:
			title_id = self.entry_field_title_id.get().upper()

			if len(title_id) > self.maxlength:
				title_id = title_id[0:self.maxlength]
			elif len(title_id) < self.maxlength:
				title_id = title_id + 'XXXXXXXX'
				title_id = title_id[0:self.maxlength]

			self.entry_field_title_id.delete(0, END)
			self.entry_field_title_id.insert(0, title_id)

			json_data['title']=str(self.entry_field_title.get())
			json_data['title_id']=title_id
			json_data['content_id']='UP0001-'+ self.entry_field_title_id.get() + '_00-0000000000000000'
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

	def generateOnChange(self, obj):
		obj.tk.eval('''
	            proc widget_proxy {widget widget_command args} {

	                # call the real tk widget command with the real args
	                set result [uplevel [linsert $args 0 $widget_command]]

	                # generate the event for certain types of commands
	                if {([lindex $args 0] in {insert replace delete}) ||
	                    ([lrange $args 0 2] == {mark set insert}) || 
	                    ([lrange $args 0 1] == {xview moveto}) ||
	                    ([lrange $args 0 1] == {xview scroll}) ||
	                    ([lrange $args 0 1] == {yview moveto}) ||
	                    ([lrange $args 0 1] == {yview scroll})} {

	                    event generate  $widget <<Change>> -when tail
	                }

	                # return the result from the real widget command
	                return $result
	            }
	            ''')
		obj.tk.eval('''
	            rename {widget} _{widget}
	            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
	        '''.format(widget=str(obj)))

	def onEntryChanged(self, event):

		new_filename = event.widget.get()
		print("Filename: " + new_filename)

		self.entry_field_iso_path.delete(0, END)
		self.entry_field_iso_path.insert(0, new_filename)

		current_filename = self.entry_field_iso_path.get()
		print("entry_field_iso_path: " + current_filename)

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
