import json
import sys
import os

from Tkinter import *
from tkFont import Font

from PIL import Image
from PIL import ImageTk
from PIL.ImageTk import PhotoImage
from PIL import ImageDraw
from PIL import ImageFont




class Main():

	def __init__(self, main):
		self.vcmd = main.register(self.validate)
		self.vcmd2 = main.register(self.validate)
		self.maxlength = 8

		# setting defaults
		self.state_drive_choice		= 'dev_hdd0'
		self.state_system_choice	= 'PS2'
		self.state_filename_choice	= ''

		self.entry_field_title_id 	= None
		self.entry_field_title 		= None
		self.entry_field_iso_path 	= None

		# canvas for image
		self.canvas = Canvas(main, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0)
		self.canvas.grid(row=0, column=0)

		# images
		self.logo_drives = []
		self.logo_drives.append(PhotoImage(Image.open("logo_drive_hdd.gif")))
		self.logo_drives.append(PhotoImage(Image.open('logo_drive_usb.gif')))

		self.logo_systems = []
		self.logo_systems.append(PhotoImage(Image.open('logo_system_PSP.gif')))
		self.logo_systems.append(PhotoImage(Image.open('logo_system_PSX.gif')))
		self.logo_systems.append(PhotoImage(Image.open('logo_system_PS2.gif')))
		self.logo_systems.append(PhotoImage(Image.open('logo_system_PS3.gif')))

		self.wallpapers = []
		self.wallpapers.append(PhotoImage(Image.open('background_light_dark_1920_1080.gif')))
		self.wallpapers.append(PhotoImage(Image.open('background_dark_1920_1080.gif')))
		self.wallpapers.append(PhotoImage(Image.open('background_light_1920_1080.gif')))
		self.wallpapers.append(PhotoImage(Image.open('background_dark_blue_symbols_1920_1080.gif')))
		self.wallpapers.append(PhotoImage(Image.open('background_light_blue_waves_1920_1080.gif')))
		self.wallpapers.append(PhotoImage(Image.open('background_light_blue_symbols_1920_1080.gif')))

		self.image_xmb_icons = Image.open('XMB_icons.png')

		self.image_pic1	= Image.open('../../pkg/PIC1.PNG')
		self.image_pic0	= Image.open('../../pkg/PIC0.PNG')
		self.image_icon0	= Image.open('../../pkg/ICON0.PNG')
		self.image_icon0 = self.image_icon0.crop((10, 10, self.image_icon0.width - 10, self.image_icon0.height - 10))



		pic1_x_scale		= 896.0/self.image_pic1.width
		pic1_y_scale		= 504.0/self.image_pic1.height

		# self.image_pic1.paste(self.image_icon0, (425, 500))
		self.image_pic1.paste(self.image_xmb_icons, (0, 0), self.image_xmb_icons)

		self.pic1_dimensions	= (int(self.image_pic1.width*pic1_x_scale), int(self.image_pic1.height*pic1_y_scale))
		self.pic0_dimensions 	= (int(pic1_x_scale * self.image_pic0.width), int(pic1_y_scale * self.image_pic0.height))
		self.icon0_dimensions 	= (int(pic1_x_scale * self.image_icon0.width), int(pic1_y_scale * self.image_icon0.height))

		game_title_test_text = 'Burnout Revenge'
		draw = ImageDraw.Draw(self.image_pic1)

		game_text_font = ImageFont.truetype('./fonts/LeelaUIb.ttf', 40)
		shadowColor = 'black'
		x = 850
		y = 475
		outlineAmount = 2
		for adj in range(outlineAmount):
			# move right
			draw.text((x - adj, y), game_title_test_text, font=game_text_font, fill=shadowColor)
			# move left
			draw.text((x + adj, y), game_title_test_text, font=game_text_font, fill=shadowColor)
			# move up
			draw.text((x, y + adj), game_title_test_text, font=game_text_font, fill=shadowColor)
			# move down
			draw.text((x, y - adj), game_title_test_text, font=game_text_font, fill=shadowColor)
			# diagnal left up
			draw.text((x - adj, y + adj), game_title_test_text, font=game_text_font, fill=shadowColor)
			# diagnal right up
			draw.text((x + adj, y + adj), game_title_test_text, font=game_text_font, fill=shadowColor)
			# diagnal left down
			draw.text((x - adj, y - adj), game_title_test_text, font=game_text_font, fill=shadowColor)
			# diagnal right down
			draw.text((x + adj, y - adj), game_title_test_text, font=game_text_font, fill=shadowColor)

		draw.text((850, 475), game_title_test_text, fill='white', font=ImageFont.truetype('./fonts/LeelaUIb.ttf', 40))


		# self.pkg_pic1	= Button(main, image=PhotoImage(self.image_pic1.resize(self.pic1_dimensions)), bd=1, bg="#000000")

		self.pkg_images = []
		self.pkg_images.append(PhotoImage(self.image_pic0.resize(self.pic0_dimensions)))
		self.pkg_images.append(PhotoImage(self.image_pic1.resize(self.pic1_dimensions)))
		self.pkg_images.append(PhotoImage(self.image_icon0.resize(self.icon0_dimensions)))

		# set first image on canvas
		self.my_image_number = 0
		self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.wallpapers[self.my_image_number])
		self.init_main_window_buttons(main)
		self.init_param_sfo_labels(main)

	def init_param_sfo_labels(self, main):
		# Constants
		text_title_id 	= 'TITLE ID'
		text_title		= 'TITLE'
		text_filename	= 'FILENAME'
		text_iso_path	= 'ISO PATH'

		height_of_text = Font(font='Helvetica').metrics('linespace')
		width_of_title_id_text 	= Font(size=15, family='Helvetica').measure(text_title_id)
		width_of_title_text 	= Font(size=15, family='Helvetica').measure(text_title)
		width_of_filename_text	= Font(size=15, family='Helvetica').measure(text_filename)
		width_of_iso_path_text 	= Font(size=15, family='Helvetica').measure(text_iso_path)

		print('height_of_text' + str(height_of_text))
		print('width_of_title_id_text' +  str(width_of_title_id_text))
		print('width_of_title_text' + str(width_of_title_text))
		print('width_of_filename_text' + str(width_of_filename_text))
		print('width_of_iso_path_text' +  str(width_of_iso_path_text))


		# paddings
		dark_side_padding		= 20
		text_box_spacing		= 4*dark_side_padding

		# coordinates
		main_offset_x_pos		= 950
		main_offset_y_pos		= 150

		title_id_text_x_pos		= main_offset_x_pos + width_of_title_id_text/2
		title_id_text_y_pos 	= main_offset_y_pos + height_of_text/2

		title_text_x_pos		= main_offset_x_pos + width_of_title_text/2
		title_text_y_pos		= dark_side_padding + title_id_text_y_pos + height_of_text

		filename_text_x_pos		= main_offset_x_pos + width_of_filename_text/2
		filename_text_y_pos		= dark_side_padding + title_text_y_pos + height_of_text

		iso_path_text_x_pos		= main_offset_x_pos + width_of_iso_path_text/2
		iso_path_text_y_pos		= dark_side_padding + filename_text_y_pos + height_of_text

		# defintions
		self.entry_field_title_id	= Entry(main, validate='key', validatecommand=(self.vcmd, '%P'))
		self.entry_field_title		= Entry(main)
		self.entry_field_filename 	= Entry(main)
		self.entry_field_iso_path	= Entry(main, state='disabled')


		# system choice buttons
		self.selection_drive_list	= ['dev_hdd0', 'dev_hdd1', 'dev_usb000']	# usb port 'x' should be selected through a list
		self.selection_system_list	= ['PSP', 'PSX', 'PS2', 'PS3']
		self.drive_path 			= self.selection_drive_list[0] 				# drive should be toggled by buttons

		self.button_HDD 	= Button(main, image=self.logo_drives[0], bd=1, command=lambda: self.on_drive_system_filename_choice_button(self.selection_drive_list[0], self.state_system_choice))
		self.button_USB 	= Button(main, image=self.logo_drives[1], bd=1, command=lambda: self.on_drive_system_filename_choice_button(self.selection_drive_list[2], self.state_system_choice))

		self.button_PSP 	= Button(main, image=self.logo_systems[0], bd=1, command=lambda: self.on_drive_system_filename_choice_button(self.state_drive_choice, self.selection_system_list[0]))
		self.button_PSX 	= Button(main, image=self.logo_systems[1], bd=1, command=lambda: self.on_drive_system_filename_choice_button(self.state_drive_choice, self.selection_system_list[1]))
		self.button_PS2 	= Button(main, image=self.logo_systems[2], bd=1, command=lambda: self.on_drive_system_filename_choice_button(self.state_drive_choice, self.selection_system_list[2]))
		self.button_PS3 	= Button(main, image=self.logo_systems[3], bd=1, command=lambda: self.on_drive_system_filename_choice_button(self.state_drive_choice, self.selection_system_list[3]))

		# self.pkg_pic1		= Button(main, image=self.pkg_images[0], bd=1, bg="#000000")
		self.pkg_pic0 		= Button(main, image=self.pkg_images[1], bd=1, bg="#000000")
		self.pkg_icon0		= Button(main, image=self.pkg_images[2], bd=1, bg="#000000")

		# dark side save-button
		self.save_button = Button(main, text="Save", command=self.on_save_button, bd=1, bg="#FBFCFB")

		# Placements
		self.title_id_text_id 	= self.canvas.create_text(title_id_text_x_pos,	title_id_text_y_pos +2,	text=text_title_id,	fill="White", font=("Helvetica", 15))
		self.title_text_id 		= self.canvas.create_text(title_text_x_pos,	title_text_y_pos	+2, text=text_title, 	fill="White", font=("Helvetica", 15))
		self.title_filename 	= self.canvas.create_text(filename_text_x_pos,	filename_text_y_pos +2, text=text_filename,	fill="White", font=("Helvetica", 15))
		self.iso_path_text_id 	= self.canvas.create_text(iso_path_text_x_pos,	iso_path_text_y_pos +2,	text=text_iso_path,	fill="White", font=("Helvetica", 15))

		self.entry_field_title_id.place(	x=text_box_spacing + iso_path_text_x_pos, y=title_id_text_y_pos	-height_of_text/3, width=200)
		self.entry_field_title.place(		x=text_box_spacing + iso_path_text_x_pos, y=title_text_y_pos		-height_of_text/3, width=200)
		self.entry_field_filename.place(	x=text_box_spacing + iso_path_text_x_pos, y=filename_text_y_pos	-height_of_text/3, width=200)
		self.entry_field_iso_path.place(	x=text_box_spacing + iso_path_text_x_pos, y=iso_path_text_y_pos	-height_of_text/3, width=200)

		self.button_HDD.place(x=main_offset_x_pos + 0 * 29, y=main_offset_y_pos - 120)
		self.button_USB.place(x=main_offset_x_pos + 3 * 29, y=main_offset_y_pos - 120)

		self.button_PSP.place(	x=main_offset_x_pos + 0 * 29, y=main_offset_y_pos -80)
		self.button_PSX.place(	x=main_offset_x_pos + 3 * 29, y=main_offset_y_pos -80)
		self.button_PS2.place(	x=main_offset_x_pos + 6 * 29, y=main_offset_y_pos -80)
		self.button_PS3.place(	x=main_offset_x_pos + 9 * 29, y=main_offset_y_pos -80)

		self.pkg_pic1	= Button(main, image=self.pkg_images[1], bd=1, bg="#000000")
		self.pkg_pic1.place(x=10, y=200)

		# self.pkg_pic1.place()
		# self.pkg_pic0.place(x=250, y=300)
		# self.pkg_pic1 = Button(main, image=self.pkg_images[1], bd=1, bg="#000000")
		self.pkg_icon0		= Button(main, image=self.pkg_images[2], bd=1, bg="#000000")
		self.pkg_icon0.place(x=210, y=400)


		self.image_pic1.paste(self.image_icon0, (425, 450), self.image_icon0)
		self.image_pic1.save('test.png')
		# test_img.paste(self.pkg_images[2], (0, 0), self.pkg_images[2])
		if "linux" not in sys.platform:
			os.startfile('test.png')
		# self.image_pic1.paste(self.image_icon0, (425, 500))

		# self.canvas.create_text(200,500,fill="white",font="Helvetica 14 italic bold",
        #                 text="This Is A Game Title")

		self.save_button.place(x=text_box_spacing + iso_path_text_x_pos, y=iso_path_text_y_pos + 20)

		####################################################################
		# Adding an onChange -listener on 'entry_field_filename'
		self.generateOnChange(self.entry_field_filename)
		self.entry_field_filename.bind('<<Change>>', self.onEntryChanged)
		####################################################################

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
		self.canvas.itemconfig(self.image_on_canvas, image=self.wallpapers[self.my_image_number])

	def on_drive_system_filename_choice_button(self, drive_choice, system_choice):
		current_iso_path 	= self.entry_field_iso_path.get()
		print('DEBUG system_choice: ' + system_choice)
		print('DEBUG drive_choice: ' + drive_choice)

		# If path is empty -> setting default values
		if current_iso_path is '':
			print('DEBUG Path is empty -> setting default values')
			self.state_drive_choice	= drive_choice
			self.state_system_choice = system_choice

			current_iso_path = '/' + self.state_drive_choice + '/' + self.state_system_choice + '/' + self.entry_field_filename.get()
			self.entry_field_iso_path.config(state=NORMAL)
			self.entry_field_iso_path.delete(0, END)
			self.entry_field_iso_path.insert(0, current_iso_path)
			self.entry_field_iso_path.config(state=DISABLED)
			print('DEBUG Default path set -> ' + self.entry_field_iso_path.get())

		# Check if drive of choice already set
		if drive_choice is self.state_drive_choice:
			print('DEBUG ' + '\'' + drive_choice + '\'' + ' already set')
		# Check if system of choice already set
		if system_choice is self.state_system_choice:
			print('DEBUG ' + '\'' + system_choice + '\'' + ' already set')


		# Replace current drive
		if drive_choice not in current_iso_path:
			print('DEBUG drive_choice not in current_iso_path')
			print('DEBUG ' + '\'' + self.state_drive_choice + '\'' + ' changed -> ' + '\'' + drive_choice + '\'')
			current_iso_path = current_iso_path.replace(self.state_drive_choice, drive_choice)
			self.entry_field_iso_path.config(state=NORMAL)
			self.entry_field_iso_path.delete(0, END)
			self.entry_field_iso_path.insert(0, current_iso_path)
			self.entry_field_iso_path.config(state=DISABLED)
			self.state_drive_choice = drive_choice

		# Replace current system
		if system_choice not in current_iso_path:
			print('DEBUG drive_choice not in current_iso_path')
			print('DEBUG ' + '\'' + self.state_system_choice + '\'' + ' changed -> ' + '\'' + system_choice + '\'')
			current_iso_path = current_iso_path.replace(self.state_system_choice, system_choice)
			self.entry_field_iso_path.config(state=NORMAL)
			self.entry_field_iso_path.delete(0, END)
			self.entry_field_iso_path.insert(0, current_iso_path)
			self.entry_field_iso_path.config(state=DISABLED)
			self.state_system_choice = system_choice



	def on_save_button(self):
		# do stuff
		self.validate_title_id()

		self.save_pkg_info_to_json()

	def save_pkg_info_to_json(self):
		with open('../util_resources/params.json.BAK') as f:
			json_data = json.load(f)

		try:
			json_data['title']=str(self.entry_field_title.get())
			json_data['title_id']=self.entry_field_title_id.get()
			json_data['content_id']='UP0001-'+ self.entry_field_title_id.get() + '_00-0000000000000000'
			json_data['iso_filepath']=str(self.entry_field_iso_path.get())

			newFile = open("../util_generated_files/webman_classics_pkg.json", "w")
			json_text = json.dumps(json_data, indent=4, separators=(",", ":"))
			newFile.write(json_text)

		except ValueError:
			print('File write error/PKGLAUNCH not found/titel_id not a string')

	# Ensure title_id doesn't exceed 8 characters
	def validate(self, P):
		if len(P) > self.maxlength:
			# re-activates listener
			main_window.after_idle(lambda: self.entry_field_title_id.config(validate='key'))
			return None  # new value too long
		else:
			print('DEBUG Title ID: ' + P)
			return True

	# Ensures title id is exactly 8 characters during save
	def validate_title_id(self):
		title_id = self.entry_field_title_id.get().upper()
		if len(title_id) < self.maxlength:
			title_id = title_id + 'XXXXXXXX'
			title_id = title_id[0:self.maxlength]

		self.entry_field_title_id.delete(0, END)
		self.entry_field_title_id.insert(0, title_id)



	# Dynamic update of the 'entry_field_filename' into the 'entry_field_iso_path'
	def onEntryChanged(self, event):
		drive = ''
		system = ''
		filename = event.widget.get()

		if self.state_drive_choice is not '':
			drive = '/' + self.state_drive_choice + '/'
		if self.state_drive_choice is not '':
			system = '/' + self.state_system_choice + '/'

		iso_path = drive + system + filename
		iso_path = iso_path.replace('//', '/')

		self.entry_field_iso_path.config(state=NORMAL)
		self.entry_field_iso_path.delete(0, END)
		self.entry_field_iso_path.insert(0, iso_path)
		self.entry_field_iso_path.config(state=DISABLED)

		current_filename = self.entry_field_iso_path.get()
		print("entry_field_iso_path: " + current_filename)

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

canvas_width = 1920
canvas_height = 1080

main_window_width = 1350
main_window_height = 720

main_window = Tk()
# changing the title of our master widget
main_window.title('webMAN Classics Maker UI')
# icon upper left corner

if "linux" not in sys.platform:
	print('linux')
	main_window.iconbitmap('../../images/webman.ico')
else:
	main_window.iconbitmap('@../../images/webman_icon.xbm')


main_window.geometry(str(main_window_width) + 'x' + str(main_window_height))
Main(main_window)

main_window.mainloop()
