import os, json, copy

from Tkinter import *
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont
from PIL.ImageTk import PhotoImage
from game_lister import Gamelist

class Main():

	def __init__(self, main):

		# canvas for image
		self.canvas = Canvas(main, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0)
		self.canvas.pack(fill=BOTH, expand=YES)

		self.main_offset_x_pos = 1325
		self.main_offset_y_pos = 150

		self.vcmd = main.register(self.dynamic_validate_title_id)
		self.vcmd2 = main.register(self.dynamic_validate_title_id)
		self.canvas_image_number = 0
		self.title_id_maxlength = len('PKGLAUNCH')
		self.tmp_title_id = ''

		# setting defaults
		self.state_drive_choice		= 'dev_hdd0'
		self.state_system_choice	= 'PS2'
		self.entry_field_iso_path 	= None

		# images
		self.logo_drives = []
		self.logo_drives.append(PhotoImage(self.small_button_maker('HDD', font='conthrax-sb.ttf', x=-4, y=0)))
		self.logo_drives.append(PhotoImage(self.small_button_maker('USB', font='conthrax-sb.ttf', x=-4, y=0)))
		self.logo_systems = []
		self.logo_systems.append(PhotoImage(self.small_button_maker('PSP', font='conthrax-sb.ttf', x=-4, y=0)))
		self.logo_systems.append(PhotoImage(self.small_button_maker('PSX', font='conthrax-sb.ttf', x=-4, y=0)))
		self.logo_systems.append(PhotoImage(self.small_button_maker('PS2', font='conthrax-sb.ttf', x=-4, y=0)))
		self.logo_systems.append(PhotoImage(self.small_button_maker('PS3', font='conthrax-sb.ttf', x=-4, y=0)))

		self.function_buttons = []
		self.function_buttons.append(PhotoImage(self.small_button_maker('Save', font='arial.ttf', x=0, y=0)))
		self.function_buttons.append(PhotoImage(self.small_button_maker('Build', font='arial.ttf', x=0, y=0)))
		self.function_buttons.append(PhotoImage(self.small_button_maker('Quit', font='arial.ttf', x=0, y=0)))
		self.function_buttons.append(PhotoImage(self.small_button_maker('Change', font='arial.ttf', x=0, y=0)))

		self.background_images = []
		self.load_backgrounds()

		# init definitions
		self.init_pkg_images()
		self.init_main_window_buttons(main)
		self.init_labels_texts_buttons(main)
		self.draw_background_on_canvas()
		self.draw_game_listbox()

	def draw_game_listbox(self):
		glist = Gamelist()
		g1 = glist.start()
		g1.place(x=1000 - 10, y=300, width=200, height=340)
		game_list = glist.get_game_list()

	def small_button_maker(self, text, **args):
		font = None
		x = None
		icon_bg_img = Image.new('RGB', (44, 20), color='black')
		for key, value in args.iteritems():
			if 'font' is key:
				font = value
			elif 'x' is key:
				x = value
			elif 'y' is key:
				val_y = value

		if not font:
			self.draw_text_on_image_w_font(icon_bg_img, text, 7, 3, 12, 'white', './resources/fonts/arial.ttf')
		else:

			if x:
				x_val = x + 12 - len(text)
			else:
				x_val = 12 - len(text)

			self.draw_text_on_image_w_font(icon_bg_img, text, x_val, 3 + val_y, 12, 'white', './resources/fonts/'+font)

		return copy.copy(icon_bg_img)


	def medium_button_maker(self, text, *font_name):
		icon_bg_img = Image.new('RGB', (54, 20), color='black')
		if not font_name:
			self.draw_text_on_image_w_font(icon_bg_img, text, 7, 1, 15, 'white', './resources/fonts/conthrax-sb.ttf')
		else:
			tmp_font = str(font_name[0])
			print(tmp_font)
			self.draw_text_on_image_w_font(icon_bg_img, text, 7, 1, 15, 'white', './resources/fonts/'+tmp_font)
		return copy.copy(icon_bg_img)

	def init_pkg_images(self):
		pic0_filename	= 'PIC0.PNG'
		pic1_filename	= 'PIC1.PNG'
		icon0_filename	= 'ICON0.PNG'

		self.image_pic0 = self.pkg_img_curr_or_def(pic0_filename)
		self.image_pic1 = self.pkg_img_curr_or_def(pic1_filename)
		self.image_icon0 = self.pkg_img_curr_or_def(icon0_filename)

		self.image_xmb_icons = Image.open('./resources/images/misc/XMB_icons.png')
		self.ps3_system_logo = Image.open('./resources/images/misc/ps3_type_logo.png')


	def pkg_img_curr_or_def(self, filename):
		pkg_image_base_path = './resources/images/pkg/'

		tmp_img_path = os.path.join(pkg_image_base_path, filename)
		print(tmp_img_path)
		if os.path.isfile(tmp_img_path):
			return Image.open(tmp_img_path)
		else:
			return Image.open(os.path.join(pkg_image_base_path, 'default'))


	def draw_background_on_canvas(self):
		self.draw_text_on_image(self.background_images[self.canvas_image_number], self.text_title_id.upper(), self.title_id_text_x_pos, self.title_id_text_y_pos, 25, 'white')
		self.draw_text_on_image(self.background_images[self.canvas_image_number], self.text_title.upper(), self.title_text_x_pos, self.title_text_y_pos, 25, 'white')
		self.draw_text_on_image(self.background_images[self.canvas_image_number], self.text_filename.upper(), self.filename_text_x_pos, self.filename_text_y_pos, 25, 'white')
		self.draw_text_on_image(self.background_images[self.canvas_image_number], self.text_iso_path.upper(), self.iso_path_text_x_pos, self.iso_path_text_y_pos, 25, 'white')

		self.current_img = self.background_images[self.canvas_image_number]
		self.current_img = self.current_img.resize((int(1920 * scaling), int(1080 * scaling)), Image.ANTIALIAS)
		self.current_background = PhotoImage(self.current_img)

		try:
			self.canvas.itemconfig(self.image_on_canvas, image=self.current_background)
		except:
			self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.current_background)

	def load_backgrounds(self):
		base_path = "./resources/images/backgrounds/"
		dark = Image.open(base_path + 'dark_transp.png')
		for files in os.walk(base_path):
			for filenames in files:
				for file in filenames:
					if 'png' in file:
						if 'dark_transp.png' not in file:
							tmp_img = Image.open(base_path+file)
							width, height = tmp_img.size
							dark = dark.resize(((600 +8), (height -115 -12)))
							tmp_img.paste(dark, (width - (610 +8), 12), dark)
							self.background_images.append(tmp_img)

	def init_labels_texts_buttons(self, main):
		# Constants
		self.text_title_id	= 'Title id'
		self.text_title 	= 'Title'
		self.text_filename	= 'Filename'
		self.text_iso_path	= 'Path'

		# paddings
		self.height_of_text = 15 #Font(font='Helvetica').metrics('linespace')
		print('self.height_of_text' + str(self.height_of_text))

		self.dark_side_padding = 20
		self.text_box_spacing = 8 * self.dark_side_padding

		# coordinates
		self.title_id_text_x_pos = self.main_offset_x_pos
		self.title_id_text_y_pos = self.main_offset_y_pos + self.height_of_text

		self.title_text_x_pos = self.main_offset_x_pos
		self.title_text_y_pos = self.dark_side_padding + self.title_id_text_y_pos + self.height_of_text

		self.filename_text_x_pos = self.main_offset_x_pos
		self.filename_text_y_pos = self.dark_side_padding + self.title_text_y_pos + self.height_of_text

		self.iso_path_text_x_pos = self.main_offset_x_pos
		self.iso_path_text_y_pos = self.dark_side_padding + self.filename_text_y_pos + self.height_of_text


		# defintions
		self.entry_field_title_id	= Entry(main, validate='key', validatecommand=(self.vcmd, '%P'))
		self.entry_field_title		= Entry(main)
		self.entry_field_filename 	= Entry(main)
		self.entry_field_iso_path	= Entry(main, state='disabled')


		# system choice buttons
		self.selection_drive_list	= ['dev_hdd0', 'dev_hdd1', 'dev_usb000']	# usb port 'x' should be selected through a list
		self.selection_system_list	= ['PSP', 'PSX', 'PS2', 'PS3']
		self.drive_path 			= self.selection_drive_list[0] 				# drive should be toggled by buttons

		self.button_HDD 	= Button(main, image=self.logo_drives[0], borderwidth=1, command=lambda: self.on_drive_and_system_button(self.selection_drive_list[0], self.state_system_choice))
		self.button_USB 	= Button(main, image=self.logo_drives[1], borderwidth=1, command=lambda: self.on_drive_and_system_button(self.selection_drive_list[2], self.state_system_choice))

		self.button_PSP 	= Button(main, image=self.logo_systems[0], borderwidth=1, command=lambda: self.on_drive_and_system_button(self.state_drive_choice, self.selection_system_list[0]))
		self.button_PSX 	= Button(main, image=self.logo_systems[1], borderwidth=1, command=lambda: self.on_drive_and_system_button(self.state_drive_choice, self.selection_system_list[1]))
		self.button_PS2 	= Button(main, image=self.logo_systems[2], borderwidth=1, command=lambda: self.on_drive_and_system_button(self.state_drive_choice, self.selection_system_list[2]))
		self.button_PS3 	= Button(main, image=self.logo_systems[3], borderwidth=1, command=lambda: self.on_drive_and_system_button(self.state_drive_choice, self.selection_system_list[3]))

		self.save_button = Button(main, image=self.function_buttons[0], borderwidth=0, command=self.on_save_button, bg="#FBFCFB")
		self.build_button = Button(main, image=self.function_buttons[1], borderwidth=0, bg="#FBFCFB")

		# Entry and Button placements
		self.entry_field_title_id.place(x=int((self.text_box_spacing + self.iso_path_text_x_pos) * scaling), y=int(self.title_id_text_y_pos	* scaling)	, width=200)
		self.entry_field_title.place(	x=int((self.text_box_spacing + self.iso_path_text_x_pos) * scaling), y=int(self.title_text_y_pos	* scaling)	, width=200)
		self.entry_field_filename.place(x=int((self.text_box_spacing + self.iso_path_text_x_pos) * scaling), y=int(self.filename_text_y_pos	* scaling)	, width=200)
		self.entry_field_iso_path.place(x=int((self.text_box_spacing + self.iso_path_text_x_pos) * scaling), y=int(self.iso_path_text_y_pos	* scaling)	, width=200)

		self.button_HDD.place(x=int((self.main_offset_x_pos + 0 * 35) * scaling), y=int(self.main_offset_y_pos - 120))
		self.button_USB.place(x=int((self.main_offset_x_pos + 3 * 35) * scaling), y=int(self.main_offset_y_pos - 120))

		self.button_PSP.place(x=int((self.main_offset_x_pos + 0 * 35) * scaling), y=int(self.main_offset_y_pos - 80))
		self.button_PSX.place(x=int((self.main_offset_x_pos + 3 * 35) * scaling), y=int(self.main_offset_y_pos - 80))
		self.button_PS2.place(x=int((self.main_offset_x_pos + 6 * 35) * scaling), y=int(self.main_offset_y_pos - 80))
		self.button_PS3.place(x=int((self.main_offset_x_pos + 9 * 35) * scaling), y=int(self.main_offset_y_pos - 80))

		# draws PIC1 and ICON0 on the canvas
		self.init_draw_images_on_canvas(main)

		if 'linux' not in sys.platform:
			# making test print of canvas
			pic1_img = Image.open('../../pkg/PIC1.PNG')
			icon_img = Image.open('../../pkg/ICON0.PNG')
			xmb_img = Image.open('./resources/images/misc/XMB_icons.png')
			pic1_img.paste(icon_img, (425, 450), icon_img)
			pic1_img.paste(xmb_img, (0, 0), xmb_img)
			self.draw_text_on_image(pic1_img, 'Burnout Revenge', 760, 490, 32, 'white')
			pic1_img.save('test.png')


		if 'linux' in sys.platform:
			button_spacing = 70
		else:
			button_spacing = 70

		self.save_button.place(x=int((self.text_box_spacing + self.iso_path_text_x_pos) * scaling), y=int((self.iso_path_text_y_pos + 40) * scaling))
		self.build_button.place(x=int((button_spacing + 10 + self.text_box_spacing + self.iso_path_text_x_pos) * scaling),y=int((self.iso_path_text_y_pos + 40) * scaling))
		##########################################################################
		# Adding an onChange -listener on 'entry_field_filename'
		self.generate_on_change(self.entry_field_filename)
		self.entry_field_filename.bind('<<Change>>', self.dynamic_filename_to_path)
		###########################################################################
		# Adding an onChange -listener on 'entry_field_title'
		self.generate_on_change(self.entry_field_title)
		self.entry_field_title.bind('<<Change>>', self.dynamic_title_to_pic1)
		###########################################################################

	def init_draw_images_on_canvas(self, main):
		pic1_x_scale = 1280.0 / self.image_pic1.width * scaling
		pic1_y_scale = 720.0 / self.image_pic1.height * scaling
		self.icon0_dimensions = (int(pic1_x_scale * self.image_icon0.width), int(pic1_y_scale * self.image_icon0.height))

		self.image_pic1.paste(self.image_xmb_icons, (0, 0), self.image_xmb_icons)
		self.image_pic1.paste(self.ps3_system_logo, (1180, 525), self.ps3_system_logo)
		self.image_pic1_xmb = copy.copy(self.image_pic1)
		self.photo_image_pic1 = PhotoImage(self.image_pic1.resize((int(1280 * scaling), int(720 * scaling)), Image.ANTIALIAS))

		self.button_pic1	= Button(main, image=self.photo_image_pic1, highlightthickness=0, bd=0)
		self.button_pic1.place(x=10 * scaling, y=245 * scaling)

		# removing 7 pixels from all sides due to transparent border
		self.image_icon0_crop 	= self.image_icon0.crop((7, 7, self.image_icon0.width - 7, self.image_icon0.height - 7))
		self.image_icon0_crop = self.image_icon0_crop.resize((self.icon0_dimensions[0] -7, self.icon0_dimensions[1] -7), Image.ANTIALIAS)

		self.photo_image_icon0 = PhotoImage(self.image_icon0_crop)

		self.button_icon0		= Button(main, image=self.photo_image_icon0, highlightthickness = 0, bd=0)
		self.button_icon0.place(x=int(285 * scaling), y=int(530 * scaling))


	def draw_text_on_image(self, image, text, text_x, text_y, text_size, text_color):
		font = ImageFont.truetype('./resources/fonts/SCE-PS3.ttf', text_size)
		draw = ImageDraw.Draw(image)
		return draw.text((text_x, text_y), text, fill=text_color, font=font)

	def draw_text_on_image_w_font(self, image, text, text_x, text_y, text_size, text_color, font):
		if not os.path.isfile(font):
			print('font does not exist')
		font = ImageFont.truetype(font, text_size)
		draw = ImageDraw.Draw(image)
		return draw.text((text_x, text_y), text, fill=text_color, font=font)

	def draw_text_on_image_w_shadow(self, image, text, text_x, text_y, text_size, text_outline, text_color, shadow_color):
		font = ImageFont.truetype('./resources/fonts/SCE-PS3.ttf', text_size)
		if text_outline == None:
			text_outline = 2
		if text_color == None:
			text_outline = 'white'
		if shadow_color == None:
			shadow_color = 'black'

		draw = ImageDraw.Draw(image)
		for adj in range(text_outline):
			# move right
			draw.text((text_x - adj, text_y), text, font=font, fill=shadow_color)
			# move left
			draw.text((text_x + adj, text_y), text, font=font, fill=shadow_color)
			# move up
			draw.text((text_x, text_y + adj), text, font=font, fill=shadow_color)
			# move down
			draw.text((text_x, text_y - adj), text, font=font, fill=shadow_color)
			# diagnal left up
			draw.text((text_x - adj, text_y + adj), text, font=font, fill=shadow_color)
			# diagnal right up
			draw.text((text_x + adj, text_y + adj), text, font=font, fill=shadow_color)
			# diagnal left down
			draw.text((text_x - adj, text_y - adj), text, font=font, fill=shadow_color)
			# diagnal right down
			draw.text((text_x + adj, text_y - adj), text, font=font, fill=shadow_color)
		return draw.text((text_x, text_y), text, fill=text_color, font=font)



	def init_main_window_buttons(self, main):
		# button to quit
		self.quit_button = Button(main, borderwidth=0, image=self.function_buttons[2], command=main.quit, bd=1)
		self.quit_button.place(x=0, y=1)

		# button to change image
		self.change_button = Button(main, borderwidth=0, image=self.function_buttons[3], command=self.on_change_button, bd=1)
		self.change_button.place(x=40+10, y=1)

	def on_change_button(self):
		# next image
		self.canvas_image_number += 1

		# return to first image
		if self.canvas_image_number == len(self.background_images):
			self.canvas_image_number = 0

		self.draw_background_on_canvas()

	def on_drive_and_system_button(self, drive_choice, system_choice):
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









	# Dynamic update of the 'entry_field_filename' into the 'entry_field_iso_path'
	def dynamic_filename_to_path(self, event):
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
		self.entry_field_iso_path.xview_moveto(1)
		self.entry_field_iso_path.config(state=DISABLED)

		current_filename = self.entry_field_iso_path.get()
		print("entry_field_iso_path: " + current_filename)


	# Dynamic update of the game title on to the PIC1 image
	def dynamic_title_to_pic1(self, event):
		tmp_img = copy.copy(self.image_pic1_xmb)
		self.draw_text_on_image(tmp_img, event.widget.get(), 760, 490, 32, 'white')
		self.photo_image_pic1_xmb = PhotoImage(tmp_img.resize((int(1280 * scaling), int(720 * scaling)), Image.ANTIALIAS))
		self.button_pic1.config(image=self.photo_image_pic1_xmb)

	def generate_on_change(self, obj):
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

	# Dynamic validation of title id
	def dynamic_validate_title_id(self, P):
		P = P.upper()
		P = P.replace('_', '')
		P = P.replace('-', '')
		self.entry_field_title_id.delete(0, END)
		self.entry_field_title_id.insert(0, P[0:self.title_id_maxlength])
		print('DEBUG Title ID: ' + self.entry_field_title_id.get())
		main_window.after_idle(lambda: self.entry_field_title_id.config(validate='key'))
		return True

	# Ensures title id is exactly 9 characters during save
	def validate_title_id_on_save(self):
		title_id = self.entry_field_title_id.get().upper()
		title_id = title_id.replace('_', '')
		title_id = title_id.replace('-', '')

		if len(title_id) is not self.title_id_maxlength:
			self.title_id_error_msg = 'Title id must be 9 characters long.'
			print(self.title_id_error_msg)
			self.entry_field_title_id.focus_set()
			self.entry_field_title_id.icursor(0)
			return False
		else:
			return True

	def validate_title_on_save(self):
		if len(self.entry_field_title.get()) > 0:
			return True
		else:
			self.title_error_msg = 'Title cannot be empty.'
			print(self.title_error_msg)
			self.entry_field_title.focus_set()
			self.entry_field_title.icursor(0)
			return False

	# Ensures title id is exactly 9 characters during save
	def validate_filename_on_save(self):
		filename = self.entry_field_filename.get()
		tmp_name = filename.lower()

		if len(tmp_name) < 1:
			self.filename_error_msg = 'The file must have a name and \'iso\' / \'bin\' extension'
			print(self.filename_error_msg)
			self.entry_field_filename.focus_set()
			self.entry_field_filename.icursor(0)
			return False

		if 'iso' in tmp_name or 'bin' in tmp_name and len(tmp_name) > 4:
			main_window.focus()
			return True


		elif 'iso' in tmp_name or 'bin' in tmp_name:
			self.filename_error_msg = 'The file must have a name'
			print(self.filename_error_msg)
			self.entry_field_filename.focus_set()
			self.entry_field_filename.icursor(0)
			return False
		else:
			self.filename_error_msg = 'Filename \'' + filename + '\' must end on \'.iso\' or \'.bin\''
			print(self.filename_error_msg)
			self.entry_field_filename.focus_set()
			self.entry_field_filename.icursor(0)
			return False

	def on_save_button(self):
		# do stuff
		if self.validate_title_id_on_save():
			print('Title_id: OK')
		else:
			return
		if self.validate_title_on_save():
			print('Title: OK')
		else:
			return
		if self.validate_filename_on_save():
			print('Title_id: OK')
		else:
			return

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
			print('File write error/PKGLAUNCH not found/title-_d not a string')

main_window = Tk()
main_window.geometry("+%d+%d" % (0, 0))

# changing the title of our master widget
main_window.title('webMAN Classics Maker UI')

# icon upper left corner
if "linux" in sys.platform:
	main_window.iconbitmap('@../../images/webman_icon.xbm')
	# scaling = 1
	scaling = 1280.0 / 1920.0

else:
	print('not linux')
	main_window.iconbitmap('../../images/webman.ico')
	# scaling = 1
	scaling = 1280.0 / 1920.0


canvas_width = int(1920* scaling)
canvas_height = int(1080* scaling)
main_window_width = int(1920* scaling)
main_window_height = int(1080* scaling)

Main(main_window)
main_window.mainloop()
