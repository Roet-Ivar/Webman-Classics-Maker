import os, json, copy, shutil, sys

# if running the webman_classics_maker.exe from root
if getattr(sys, 'frozen', False):
	sys.path.append(os.path.join(os.path.dirname(sys.executable), 'resources', 'tools', 'util_scripts'))
	sys.path.append(os.path.join(os.path.dirname(sys.executable), 'resources', 'tools', 'util_scripts', 'wcm_gui'))
else:
	# running webman_classics_maker.py from root
	app_full_path = os.path.realpath(__file__)
	application_path = os.path.dirname(app_full_path)
	sys.path.append(os.path.join(application_path, 'resources', 'tools', 'util_scripts'))
	sys.path.append(os.path.join(application_path, 'resources', 'tools', 'util_scripts', 'wcm_gui'))
from global_paths import App as AppPaths
from global_paths import Image as ImagePaths

sys.path.append(AppPaths.settings)

try:
	# Python2
	from Tkinter import *
	import Tkinter as tk
	import ttk
except ImportError as e:
	print("Tkinter import error: " + e.message)
	# Python3
	from tkinter import *
	import tkinter as tk
	import ttk


from PIL import Image, ImageDraw, ImageFont
from PIL.ImageTk import PhotoImage
from tkFileDialog import askopenfile
from game_listbox import Gamelist
# from ftp_game_list_fetcher import FtpGameList
from ftp_game_data_fetcher import FtpGameList

# check python version higher than 2
if sys.version_info[0] > 2:
	print("""Error: Webman Classics Maker is only compatible with python 2.7 32/64.
		  Reason: the pkgcrypt module hasn't been ported to python 3.x""")
	sys.exit(1)

from build_all_scripts import Webman_PKG as Webman_PKG


class Main:
	def __init__(self):
		self.main = main_window

		# common paths
		self.WCM_BASE_PATH 		= AppPaths.wcm_gui
		self.pkg_dir 			= AppPaths.pkg
		self.wcm_work_dir 		= AppPaths.wcm_work_dir
		self.wcm_pkg_dir 		= os.path.join(self.wcm_work_dir, 'pkg')
		self.builds_path 		= AppPaths.builds
		self.ftp_settings_path 	= os.path.join(AppPaths.settings, 'ftp_settings.cfg')
		self.fonts_path 		= AppPaths.fonts

		# self.main_offset_x_pos = 1325
		self.main_offset_x_pos = 1450
		self.main_offset_y_pos = 50

		self.window_x_width = 1280.0
		self.window_y_width = 720.0

		# canvas for image
		self.canvas = Canvas(self.main, width=canvas_width, height=canvas_height, borderwidth=0, highlightthickness=0)
		self.canvas.pack(fill=BOTH, expand=YES)

		self.vcmd = self.main.register(self.dynamic_validate_title_id)
		self.vcmd2 = self.main.register(self.dynamic_validate_title_id)
		self.canvas_image_number = 0
		self.title_id_maxlength = len('PKGLAUNCH')
		self.tmp_title_id = ''

		self.drive_system_array = ['drive', 'system']

		self.entry_field_iso_path 	= None

		self.usb_port_number 		= 0

		# images
		self.images_logo_drive = []
		self.images_logo_drive.append(PhotoImage(self.smaller_button_maker('HDD', font='conthrax-sb.ttf', x=-1, y=-2)))
		self.images_logo_drive.append(PhotoImage(self.smaller_button_maker('USB', font='conthrax-sb.ttf', x=-1, y=-2)))

		self.images_logo_system = []
		self.images_logo_system.append(PhotoImage(self.smaller_button_maker('PSP', font='conthrax-sb.ttf', x=-1, y=-2)))
		self.images_logo_system.append(PhotoImage(self.smaller_button_maker('PSX', font='conthrax-sb.ttf', x=-1, y=-2)))
		self.images_logo_system.append(PhotoImage(self.smaller_button_maker('PS2', font='conthrax-sb.ttf', x=-1, y=-2)))
		self.images_logo_system.append(PhotoImage(self.smaller_button_maker('PS3', font='conthrax-sb.ttf', x=-1, y=-2)))

		self.images_function_button = []
		self.images_function_button.append(PhotoImage(self.small_button_maker('Save', font='arial.ttf', x=3, y=0)))
		self.images_function_button.append(PhotoImage(self.small_button_maker('Build', font='arial.ttf', x=3, y=0)))
		self.images_function_button.append(PhotoImage(self.small_button_maker('Quit', font='arial.ttf', x=3, y=0)))
		self.images_function_button.append(PhotoImage(self.small_button_maker('Change', font='arial.ttf', x=-3, y=0)))

		self.images_gamelist_button = []
		self.images_gamelist_button.append(PhotoImage(self.small_button_maker('Fetch', font='arial.ttf', x=3, y=0)))
		self.images_gamelist_button.append(PhotoImage(self.small_button_maker('Refresh', font='arial.ttf', x=-1, y=0)))

		self.background_images = []
		self.load_backgrounds()

		# buttons
		self.button_icon0	 = None
		self.button_pic0 	 = None
		self.button_pic1	 = None

		self.button_HDD 	 = None
		self.button_USB 	 = None

		self.button_PSP 	 = None
		self.button_PSX 	 = None
		self.button_PS2 	 = None
		self.button_PS3 	 = None

		self.build_button 	 = None
		self.save_button 	 = None

		self.ftp_sync_button			= None
		self.game_list_refresh_button	= None


		# text tooltip messages
		self.USB_BUTTON_TOOLTIP_MSG = "toggle USB port (0-3)"
		self.SAVE_BUTTON_TOOLTIP_MSG = "save 'work_dir' folder"
		self.BUILD_BUTTON_TOOLTIP_MSG = "build and save the PKG"
		self.SYNC_BUTTON_TOOLTIP_MSG = "fetch gamelist over FTP"
		self.REFRESH_BUTTON_TOOLTIP_MSG = "reload gamelist from disk"
		self.ICON0_TOOLTIP_MSG = "Click to change ICON0"
		self.PIC0_TOOLTIP_MSG = "Click to change  PIC0"
		self.PIC1_TOOLTIP_MSG = "Click to change  PIC1"

		# init definitions
		self.init_config_file()
		self.init_wcm_work_dir()
		self.init_pkg_images()

		# self.init_main_window_buttons(self.main)
		self.init_default_view(self.main)
		self.draw_background_on_canvas()

		self.list_filter_platform = 'All'
		self.create_list_combo_box(self.list_filter_platform)

	# definitions starts here
	def init_wcm_work_dir(self):
		# clean and init wcm_work_dir in startup
		if os.path.isdir(AppPaths.wcm_work_dir):
			shutil.rmtree(AppPaths.wcm_work_dir)
			os.makedirs(os.path.join(AppPaths.wcm_work_dir, 'pkg'))

			self.init_pkg_images()

	def init_config_file(self):
		if not os.path.isdir(AppPaths.settings):
			os.mkdir(AppPaths.settings)
			if os.path.isfile(os.path.join(AppPaths.util_resources, 'ftp_settings.cfg.BAK')):
				shutil.copyfile(os.path.join(AppPaths.util_resources, 'ftp_settings.cfg.BAK'), self.ftp_settings_path)
			else:
				print('Error: ' + os.path.join(AppPaths.util_resources, 'ftp_settings.cfg.BAK') + ' could not be find.')

		with open(self.ftp_settings_path, 'r') as settings_file:
			self.ftp_settings_data = json.load(settings_file)

	def get_ftp_ip_from_config(self):
		return self.ftp_settings_data['ps3_lan_ip']

	def get_ftp_user_from_config(self):
		return self.ftp_settings_data['ftp_user']

	def get_ftp_pass_from_config(self):
		return self.ftp_settings_data['ftp_password']


	def create_list_combo_box(self, platform):
		# create the listbox (games list)
		self.gamelist = Gamelist(platform)
		game_list_frame = self.gamelist.create_main_frame(self.entry_field_title_id, self.entry_field_title, self.entry_field_filename, self.entry_field_iso_path, self.drive_system_array)
		game_list_frame.place(x=int((self.main_offset_x_pos) * scaling),
							  y=self.main_offset_y_pos + 220,
							  width=270,
							  height=300)

		self.game_list_box = self.gamelist.get_listbox()
		self.game_list_box.config(selectmode='SINGLE',
								  activestyle='dotbox',
								  borderwidth=0)

		# insert the dropdown into the listbox
		from platform_dropdown import Dropdown
		self.dropdown = Dropdown(self.canvas, self.game_list_box, 1100, 247).get_box()
		self.dropdown.bind("<<ComboboxSelected>>", self.box_filter_callback)


	def box_filter_callback(self, event):
		self.list_filter_platform = event.widget.get()
		self.create_list_combo_box(self.list_filter_platform)
		self.dropdown.set(self.list_filter_platform)
		self.game_list_box.focus()


	def smaller_button_maker(self, text, **args):
		font = None
		x = None
		icon_bg_img = Image.new('RGB', (44, 15), color='black')
		for key, value in args.iteritems():
			if 'font' is key:
				font = value
			elif 'x' is key:
				x = value
			elif 'y' is key:
				y = value
			elif 'width' is key:
				width = value
			elif 'height' is key:
				height = value

		if not font:
			self.draw_text_on_image_w_font(icon_bg_img, text, 7, 3, 12, 'white',
										   os.path.join(self.fonts_path, 'arial.ttf'))
		else:

			if x:
				x_val = x + 12 - len(text)
			else:
				x_val = 12 - len(text)

			self.draw_text_on_image_w_font(icon_bg_img, text, x_val, 3 + y, 10, 'white',
										   os.path.join(self.fonts_path, font))

		return copy.copy(icon_bg_img)

	def small_button_maker(self, text, **args):
		font = None
		x = None
		icon_bg_img = Image.new('RGB', (50, 20), color='black')
		for key, value in args.iteritems():
			if 'font' is key:
				font = value
			elif 'x' is key:
				x = value
			elif 'y' is key:
				y = value
			elif 'width' is key:
				width = value
			elif 'height' is key:
				height = value

		if not font:
			self.draw_text_on_image_w_font(icon_bg_img, text, 7, 3, 12, 'white',
										   os.path.join(self.fonts_path, 'arial.ttf'))
		else:

			if x:
				x_val = x + 12 - len(text)
			else:
				x_val = 12 - len(text)

			self.draw_text_on_image_w_font(icon_bg_img, text, x_val, 3 + y, 12, 'white',
										   os.path.join(self.fonts_path, font))

		return copy.copy(icon_bg_img)

	def medium_button_maker(self, text, *font_name):
		icon_bg_img = Image.new('RGB', (54, 20), color='black')
		if not font_name:
			self.draw_text_on_image_w_font(icon_bg_img, text, 7, 1, 15, 'white',
										   os.path.join(self.fonts_path, 'conthrax-sb.ttf'))
		else:
			tmp_font = str(font_name[0])
			self.draw_text_on_image_w_font(icon_bg_img, text, 7, 1, 15, 'white',
										   os.path.join(self.fonts_path, tmp_font))
		return copy.copy(icon_bg_img)

	def init_pkg_images(self):
		icon0_filename = 'ICON0.PNG'
		pic0_filename = 'PIC0.PNG'
		pic1_filename = 'PIC1.PNG'

		self.image_icon0 = self.load_pkg_images(icon0_filename)
		self.image_icon0_ref = copy.copy(self.image_icon0)

		self.image_pic0 = self.load_pkg_images(pic0_filename)
		self.image_pic0_ref = copy.copy(self.image_pic0)

		self.image_pic1 = self.load_pkg_images(pic1_filename)
		self.image_pic1_ref = copy.copy(self.image_pic0)
		# self.photo_image_pic1_xmb = copy.copy(self.image_pic1)
		self.image_pic1_w_title = copy.copy(self.image_pic1)

		self.pkg_icon0 = None
		self.pkg_pic0 = None
		self.pkg_pic1= None

		self.image_xmb_icons = Image.open(os.path.join(ImagePaths.xmb, 'XMB_icons.png'))
		self.ps3_system_logo = Image.open(os.path.join(ImagePaths.xmb, 'ps3_type_logo.png'))

	def load_pkg_images(self, filename):
		default_pkg_img_dir = os.path.join(ImagePaths.pkg, 'default')
		png_path = os.path.join(self.wcm_pkg_dir, filename)

		if '.png' in png_path.lower() and os.path.isfile(png_path):
			return Image.open(png_path).convert("RGBA")
		else:
			shutil.copyfile(os.path.join(default_pkg_img_dir, filename), png_path)
			return Image.open(png_path).convert("RGBA")

	def draw_background_on_canvas(self):
		self.current_img = self.background_images[self.canvas_image_number]
		webman_logo = Image.open(os.path.join(ImagePaths.misc, 'webman_text_icon_bw.png')).resize(
			(int(464 * 0.45), int(255 * 0.45)))

		self.draw_text_on_image_w_shadow(self.background_images[self.canvas_image_number], 'webMAN',
										 490, -10, 110, 6, '#0C55F4', 'black',
										 font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_shadow(self.background_images[self.canvas_image_number], 'Classics Maker',
										 422, 60, 80, 5, 'white', 'black',
										 font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.current_img.paste(webman_logo, (515, 22), webman_logo)

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number], self.text_device.upper(),
									   self.main_offset_x_pos, self.device_text_y_pos, 25, 'white',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number], self.text_platform.upper(),
									   self.main_offset_x_pos, self.type_text_y_pos, 25, 'white',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number], self.text_title_id.upper(),
									   self.main_offset_x_pos, self.title_id_text_y_pos, 25, 'white',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number], self.text_title.upper(),
									   self.main_offset_x_pos, self.title_text_y_pos, 25, 'white',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number], self.text_filename.upper(),
									   self.main_offset_x_pos, self.filename_text_y_pos, 25, 'white',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number], self.text_iso_path.upper(),
									   self.main_offset_x_pos, self.iso_path_text_y_pos, 25, 'white',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number],
									   self.text_ftp_game_list.upper(),
									   self.main_offset_x_pos, self.iso_path_text_y_pos + 120, 25, 'white',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number], self.text_ps3_ip_label.upper(),
									   self.main_offset_x_pos + 0 * 50, self.main_offset_y_pos + 810, 25, '#ffffff',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number],
									   self.text_ps3_usr_label.upper(),
									   self.main_offset_x_pos + 5 * 50, self.main_offset_y_pos + 810, 25, '#ffffff',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.draw_text_on_image_w_font(self.background_images[self.canvas_image_number],
									   self.text_ps3_pass_label.upper(),
									   self.main_offset_x_pos + 5 * 50, self.main_offset_y_pos + 845, 25, '#ffffff',
									   font=os.path.join(self.fonts_path, 'LLPIXEL3.ttf'))

		self.current_img = self.background_images[self.canvas_image_number]
		self.current_img = self.current_img.resize((int(1920 * scaling), int(1080 * scaling)), Image.ANTIALIAS)

		self.tv_frame = Image.open(
			os.path.join(ImagePaths.misc, 'tv_frame_1080_ps3_3.png')).resize(
			(int(1990 * scaling), int(1327 * scaling)), Image.ANTIALIAS)
		self.current_img.paste(self.tv_frame, (int(45 * scaling), int(143 * scaling)), self.tv_frame)

		self.current_background = PhotoImage(self.current_img)

		try:
			self.canvas.itemconfig(self.image_on_canvas, image=self.current_background)
		except:
			self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.current_background)

	def load_backgrounds(self):
		base_path = os.path.join(ImagePaths.images, 'backgrounds')
		dark = Image.open(os.path.join(base_path, 'dark_transp.png'))
		for files in os.walk(base_path):
			for filenames in files:
				for file in filenames:
					if any(ext in file for ext in ['png', 'jpg']):
						# we dont want the dark transparency image to be a background
						if 'dark_transp.png' not in file:
							tmp_img = Image.open(os.path.join(base_path, base_path, file))
							width, height = tmp_img.size
							dark = dark.resize(((470 + 8), (height - 115 - 12)))
							tmp_img.paste(dark, (width - (480 + 8), 12), dark)
							self.background_images.append(tmp_img)

	def init_default_view(self, main):
		# Constants
		self.text_device			= 'Device'
		self.text_platform			= 'Type'

		self.text_title_id			= 'Title id'
		self.text_title				= 'Title'
		self.text_filename			= 'Filename'
		self.text_iso_path			= 'Path'

		self.text_ftp_game_list		= 'FTP Game list'
		self.text_ps3_ip_label		= 'PS3-ip'
		self.text_ps3_usr_label		= 'User'
		self.text_ps3_pass_label	= 'Pass'

		# Paddings
		self.height_of_text		 = 15  # Font(font='Helvetica').metrics('linespace')
		self.dark_side_x_padding = 20
		self.dark_side_y_padding = 20

		self.text_box_spacing = 7 * self.dark_side_x_padding

		# gui text coordinates
		self.device_text_y_pos = self.main_offset_y_pos + self.height_of_text
		self.type_text_y_pos = self.dark_side_y_padding + self.device_text_y_pos + self.height_of_text
		self.title_id_text_y_pos = self.dark_side_y_padding + 7 + self.type_text_y_pos + self.height_of_text + 2
		self.title_text_y_pos = self.dark_side_y_padding + self.title_id_text_y_pos + self.height_of_text
		self.filename_text_y_pos = self.dark_side_y_padding + self.title_text_y_pos + self.height_of_text
		self.iso_path_text_y_pos = self.dark_side_y_padding + self.filename_text_y_pos + self.height_of_text - 1

		# image buttons coordinates (w/o res scaling)
		self.pic1_button_x_pos = 75
		self.pic1_button_y_pos = 175
		self.pic0_button_x_pos = 573
		self.pic0_button_y_pos = 450
		self.icon0_button_x_pos = 344
		self.icon0_button_y_pos = 454

		# image coordinates for the gui
		self.icon0_x_pos = 405
		self.icon0_y_pos = 416
		self.pic0_x_pos = 750
		self.pic0_y_pos = 412

		# entry fields
		self.entry_field_title_id 	= Entry(main, validate='key', validatecommand=(self.vcmd, '%P'))
		self.entry_field_title 		= Entry(main)
		self.entry_field_filename 	= Entry(main)
		self.entry_field_iso_path 	= Entry(main, state='readonly')

		##########################################################################
		# Adding an on_change-listener on 'entry_field_filename'
		self.generate_on_change(self.entry_field_filename)
		self.entry_field_filename.bind('<<Change>>', self.dynamic_filename_to_path)
		###########################################################################
		# Adding an on_change-listener on 'entry_field_title'
		self.generate_on_change(self.entry_field_title)
		self.entry_field_title.bind('<<Change>>', self.dynamic_title_to_pic1)
		###########################################################################

		self.entry_field_ftp_ip = Entry(main)
		self.entry_field_ftp_ip.insert(0, self.get_ftp_ip_from_config())

		self.entry_field_ftp_user = Entry(main)
		self.entry_field_ftp_user.insert(0, self.get_ftp_user_from_config())

		self.entry_field_ftp_pass = Entry(main)
		self.entry_field_ftp_pass.insert(0, self.get_ftp_pass_from_config())

		# system choice buttons
		self.selection_drive_list = ['dev_hdd0',
									 'dev_usb000', 'dev_usb001', 'dev_usb002',
									 'dev_usb003']  # usb port 'x' should be selected through a list
		self.selection_system_list = ['PSPISO', 'PSXISO', 'PS2ISO', 'PS3ISO']
		self.drive_path = self.selection_drive_list[0]  # drive should be toggled by buttons

		self.button_HDD = Button(main,
								 image=self.images_logo_drive[0],
								 borderwidth=1,
								 command=lambda: self.on_drive_button(self.selection_drive_list[0]))

		self.button_USB = Button(main,
								 image=self.images_logo_drive[1],
								 borderwidth=1,
								 command=lambda:
								 self.on_drive_button(self.selection_drive_list[self.usb_port_number + 1]))

		self.button_PSP = Button(main,
								 image=self.images_logo_system[0],
								 borderwidth=1,
								 command=lambda:
								 self.on_system_button(self.drive_system_array[0], self.selection_system_list[0]))

		self.button_PSX = Button(main,
								 image=self.images_logo_system[1],
								 borderwidth=1,
								 command=lambda:
								 self.on_system_button(self.drive_system_array[0], self.selection_system_list[1]))

		self.button_PS2 = Button(main,
								 image=self.images_logo_system[2],
								 borderwidth=1,
								 command=lambda:
								 self.on_system_button(self.drive_system_array[0], self.selection_system_list[2]))

		self.button_PS3 = Button(main,
								 image=self.images_logo_system[3],
								 borderwidth=1,
								 command=lambda:
								 self.on_system_button(self.drive_system_array[0], self.selection_system_list[3]))

		self.save_button = Button(main,
								  image=self.images_function_button[0],
								  borderwidth=0,
								  command=self.validate_fields,
								  bg="#FBFCFB")

		self.build_button = Button(main,
								   image=self.images_function_button[1],
								   borderwidth=0,
								   command=self.on_build_button,
								   bg="#FBFCFB")

		self.ftp_sync_button = Button(main,
									  image=self.images_gamelist_button[0],
									  borderwidth=0,
									  command=self.on_ftp_fetch_button,
									  bg="#FBFCFB")


		self.game_list_refresh_button = Button(main,
											   image=self.images_gamelist_button[1],
											   borderwidth=0,
											   command=self.on_game_list_refresh,
											   bg="#FBFCFB")

		# button tooltips
		CreateToolTip(self.button_USB, self.USB_BUTTON_TOOLTIP_MSG)
		CreateToolTip(self.save_button, self.SAVE_BUTTON_TOOLTIP_MSG)
		CreateToolTip(self.build_button, self.BUILD_BUTTON_TOOLTIP_MSG)
		CreateToolTip(self.ftp_sync_button, self.SYNC_BUTTON_TOOLTIP_MSG)
		CreateToolTip(self.game_list_refresh_button, self.REFRESH_BUTTON_TOOLTIP_MSG)

		# Entry field placements
		entry_field_width = 200
		self.entry_field_title_id.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * scaling),
										y=int(self.title_id_text_y_pos * scaling),
										width=entry_field_width)

		self.entry_field_title.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * scaling),
									 y=int(self.title_text_y_pos * scaling),
									 width=entry_field_width)

		self.entry_field_filename.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * scaling),
										y=int(self.filename_text_y_pos * scaling),
										width=entry_field_width)

		self.entry_field_iso_path.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * scaling),
										y=int(self.iso_path_text_y_pos * scaling),
										width=entry_field_width)

		self.entry_field_ftp_ip.place(x=int((self.main_offset_x_pos + 90) * scaling),
									  y=int((self.main_offset_y_pos + 815) * scaling),
									  width=90)

		self.entry_field_ftp_user.place(x=int((self.main_offset_x_pos + 320) * scaling),
										y=int((self.main_offset_y_pos + 815) * scaling),
										width=60)

		self.entry_field_ftp_pass.place(x=int((self.main_offset_x_pos + 320) * scaling),
										y=int((self.main_offset_y_pos + 850) * scaling),
										width=60)

		# Button placements
		self.button_HDD.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 0 * 75) * scaling),
							  y=int(self.device_text_y_pos * scaling))

		self.button_USB.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 1 * 75) * scaling),
							  y=int(self.device_text_y_pos * scaling))

		self.button_PSP.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 0 * 75) * scaling),
							  y=int(self.type_text_y_pos * scaling))

		self.button_PSX.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 1 * 75) * scaling),
							  y=int(self.type_text_y_pos * scaling))

		self.button_PS2.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 2 * 75) * scaling),
							  y=int(self.type_text_y_pos * scaling))

		self.button_PS3.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 3 * 75) * scaling),
							  y=int(self.type_text_y_pos * scaling))

		# draws ICON0, PIC0 and PIC1 on the canvas
		self.init_draw_images_on_canvas(main)

		self.button_spacing = 70

		self.save_button.place(
			x=int((self.text_box_spacing + self.main_offset_x_pos) * scaling),
			y=int((self.iso_path_text_y_pos + 40) * scaling))

		self.build_button.place(
			x=int((self.button_spacing + 10 + self.text_box_spacing + self.main_offset_x_pos) * scaling),
			y=int((self.iso_path_text_y_pos + 40) * scaling))

		self.ftp_sync_button.place(
			x=int((self.main_offset_x_pos) * scaling),
			y=int((self.main_offset_y_pos + 855) * scaling))

		self.game_list_refresh_button.place(
			x=int((self.main_offset_x_pos + 80) * scaling),
			y=int((self.main_offset_y_pos + 855) * scaling))



	def init_draw_images_on_canvas(self, main, *args, **kwargs):
		img_to_be_changed = kwargs.get('img_to_be_changed', None)
		pkg_build_path = kwargs.get('pkg_build_path', None)

		pic1_changed = False
		# TODO image replace browser: missing the title text!
		if img_to_be_changed is not None:
			if img_to_be_changed.lower() == 'pic1':
				pic1_changed = True
				self.draw_text_on_image_w_shadow(self.image_pic1, self.entry_field_title.get(), 745, 457, 32, 2, 'white', 'black')

				self.photo_image_pic1_xmb = PhotoImage(
					self.image_pic1.resize((int(1280 * scaling), int(720 * scaling)), Image.ANTIALIAS))

				self.button_pic1.config(image=self.photo_image_pic1_xmb)
				self.image_pic0 = self.image_pic0_ref
				self.image_icon0 = self.image_icon0_ref


		# check if xmb_icons needs to be re-drawn
		elif pkg_build_path is not None:
			if os.path.exists(pkg_build_path):
				# draw PIC1 from pkg_dir and then xmb icons and system logo onto the pkg  background
				if os.path.isfile(os.path.join(pkg_build_path, 'ICON0.PNG')):
					self.image_icon0 = Image.open(os.path.join(pkg_build_path, 'ICON0.PNG')).convert("RGBA")
				else:
					self.image_icon0 = Image.open(os.path.join(self.wcm_pkg_dir, 'ICON0.PNG')).convert("RGBA")

				if os.path.isfile(os.path.join(pkg_build_path, 'PIC0.PNG')):
					self.image_pic0 = Image.open(os.path.join(pkg_build_path, 'PIC0.PNG')).convert("RGBA")
				else:
					self.image_pic0 = Image.open(os.path.join(self.wcm_pkg_dir, 'PIC0.PNG')).convert("RGBA")

				if os.path.isfile(os.path.join(pkg_build_path, 'PIC1.PNG')):
					self.image_pic1 = Image.open(os.path.join(pkg_build_path, 'PIC1.PNG')).convert("RGBA")
					self.image_pic1_ref = Image.open(os.path.join(pkg_build_path, 'PIC1.PNG')).convert("RGBA")
					pic1_changed = True
				else:
					self.image_pic1 = Image.open(os.path.join(self.wcm_pkg_dir, 'PIC1.PNG')).convert("RGBA")
					self.image_pic1_ref = Image.open(os.path.join(self.wcm_pkg_dir, 'PIC1.PNG')).convert("RGBA")
					pic1_changed = True
		else:
			self.image_pic1 = Image.open(os.path.join(self.wcm_pkg_dir, 'PIC1.PNG')).convert("RGBA")
			self.image_pic1_ref = Image.open(os.path.join(self.wcm_pkg_dir, 'PIC1.PNG')).convert("RGBA")
			pic1_changed = True

		if pic1_changed:
			# draw xmb icons and system logo onto the background
			self.image_pic1.paste(self.image_xmb_icons, (0, 0), self.image_xmb_icons)
			self.image_pic1.paste(self.ps3_system_logo, (1180, 525), self.ps3_system_logo)


		# crop and blend ICON0 to the background
		tmp_icon0_bg = copy.copy(self.image_pic1_ref)
		tmp_icon0_bg.paste(self.image_icon0.convert("RGBA"), (self.icon0_x_pos, self.icon0_y_pos), self.image_icon0.convert("RGBA"))
		# Image.crop((left, top, right, bottom))
		tmp_image_icon0 = tmp_icon0_bg.crop((self.icon0_x_pos, self.icon0_y_pos,
											 self.icon0_x_pos + self.image_icon0.width,
											 self.icon0_y_pos + self.image_icon0.height))


		# crop and blend PIC0 to the background
		if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC0.PNG')):
			tmp_pic0_bg = copy.copy(self.image_pic1_ref)
		else:
			tmp_pic0_bg = copy.copy(self.image_pic1_w_title)
		# Image.paste(im1, (left, top, right, bottom), im1)
		tmp_pic0_bg.paste(self.image_pic0, (self.pic0_x_pos, self.pic0_y_pos), self.image_pic0)
		# Image.crop((left, top, right, bottom))
		tmp_image_pic0 = tmp_pic0_bg.crop((self.pic0_x_pos, self.pic0_y_pos,
										   self.pic0_x_pos + self.image_pic0.width,
										   self.pic0_y_pos + self.image_pic0.height))

		# draw launch-date and clock beside ICON0
		self.draw_text_on_image_w_shadow(self.image_pic1, "11/11/2006 00:00", 760, 522, 20, 1, 'white', 'black')

		# resize: ->853, ->480
		self.photoimage_pic1 = PhotoImage(
			self.image_pic1.resize((int(1280 * scaling), int(720 * scaling)), Image.ANTIALIAS))

		self.button_pic1 = Button(main,
								  image=self.photoimage_pic1,
								  highlightthickness=0,
								  bd=0,
								  command=lambda: self.image_replace_browser(main))
		CreateToolTip(self.button_pic1, self.PIC1_TOOLTIP_MSG)

		# ICON0 resizing
		icon0_x_scale = self.window_x_width / self.image_pic1.width * scaling
		icon0_y_scale = self.window_y_width / self.image_pic1.height * scaling

		self.icon0_new_dim = (
			int(icon0_x_scale * tmp_image_icon0.width), int(icon0_y_scale * tmp_image_icon0.height))

		self.image_icon0_resize = copy.copy(tmp_image_icon0)
		self.image_icon0_resize = self.image_icon0_resize.resize(
			(self.icon0_new_dim[0], self.icon0_new_dim[1]), Image.ANTIALIAS)

		self.photoimage_icon0 = PhotoImage(self.image_icon0_resize)
		self.button_icon0 = Button(main,
								   image=self.photoimage_icon0,
								   highlightthickness=0,
								   bd=0,
								   command=lambda: self.image_replace_browser(main))
		CreateToolTip(self.button_icon0, self.ICON0_TOOLTIP_MSG)

		# PIC0 resizing
		pic0_x_scale = self.window_x_width / self.image_pic1.width * scaling
		pic0_y_scale = self.window_y_width / self.image_pic1.height * scaling

		self.pic0_new_dim = (
			int(pic0_x_scale * tmp_image_pic0.width), int(pic0_y_scale * tmp_image_pic0.height))

		self.image_pic0_resize = copy.copy(tmp_image_pic0)
		self.image_pic0_resize = self.image_pic0_resize.resize(
			(self.pic0_new_dim[0], self.pic0_new_dim[1]), Image.ANTIALIAS)

		self.photo_image_pic0 = PhotoImage(self.image_pic0_resize)
		self.button_pic0 = Button(main,
								   image=self.photo_image_pic0,
								   highlightthickness=0,
								   bd=0,
								   command=lambda: self.image_replace_browser(main))
		CreateToolTip(self.button_pic0, self.PIC0_TOOLTIP_MSG)


		# finally placing ICON0, PIC0 and PIC1 onto the canvas
		self.button_pic1.place(x=self.pic1_button_x_pos * scaling, y=self.pic1_button_y_pos * scaling)
		self.button_pic0.place(x=int(self.pic0_button_x_pos * scaling), y=int(self.pic0_button_y_pos * scaling))
		self.button_icon0.place(x=int(self.icon0_button_x_pos * scaling), y=int(self.icon0_button_y_pos * scaling))

	def draw_text_on_image(self, image, text, text_x, text_y, text_size, text_color):
		font = ImageFont.truetype(os.path.join(self.fonts_path, 'SCE-PS3.ttf'), text_size)
		draw = ImageDraw.Draw(image)
		return draw.text((text_x, text_y), text, fill=text_color, font=font)

	def draw_text_on_image_w_font(self, image, text, text_x, text_y, text_size, text_color, font):
		if not os.path.isfile(font):
			print('font does not exist')
		font = ImageFont.truetype(font, text_size)
		draw = ImageDraw.Draw(image)
		return draw.text((text_x, text_y), text, fill=text_color, font=font)

	def draw_text_on_image_w_shadow(self, image, text, text_x, text_y, text_size, text_outline, text_color,
									shadow_color, **args):
		if 'font' in args:
			font = ImageFont.truetype(args['font'], text_size)
		else:
			font = ImageFont.truetype(os.path.join(self.fonts_path, 'SCE-PS3.ttf'), text_size)

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

	# def init_main_window_buttons(self, main):
		# button to change image
		# self.change_button = Button(main,
		# 							borderwidth=0,
		# 							image=self.images_function_button[3],
		# 							command=self.on_change_button,
		# 							bd=1)
		# self.change_button.place(x=40 + 13, y=1)

	def on_change_button(self):
		# next image
		self.canvas_image_number += 1

		# return to first image
		if self.canvas_image_number == len(self.background_images):
			self.canvas_image_number = 0

		self.draw_background_on_canvas()

	def on_drive_button(self, drive_choice):
		print('DEBUG on_drive_button')
		# Check if same drive already set
		if drive_choice in self.entry_field_iso_path.get():
			print('DEBUG ' + '\'' + drive_choice + '\'' + ' already set')
			# if dev_usb### already set -> iterate port (0-3)
			if 'dev_usb00' in drive_choice:
				self.usb_port_number = self.usb_port_number + 1

				if self.usb_port_number > 3:
					self.usb_port_number = 0
				print('DEBUG usb_port_number: ' + str(self.usb_port_number))
				drive_choice = 'dev_usb00' + str(self.usb_port_number)

		print('DEBUG drive_choice: ' + drive_choice)
		self.drive_system_array[0] = drive_choice

		current_iso_path = '/' + self.drive_system_array[0] + '/' + self.drive_system_array[1] + '/' + self.entry_field_filename.get()
		self.update_iso_path_entry_field(current_iso_path)

	def on_system_button(self, drive_choice, system_choice):
		print('DEBUG on_system_button')
		if system_choice in self.entry_field_iso_path.get():
			print('DEBUG ' + '\'' + system_choice + '\'' + ' already set')

		print('DEBUG system_choice: ' + system_choice)
		self.drive_system_array[1] = system_choice

		current_iso_path = '/' + str(self.drive_system_array[0]) + '/' + str(self.drive_system_array[1]) + '/' + self.entry_field_filename.get()
		self.update_iso_path_entry_field(current_iso_path)

		# Replace current drive
		if drive_choice not in current_iso_path:
			print('DEBUG drive_choice not in current_iso_path')
			print('DEBUG ' + '\'' + self.drive_system_array[0] + '\'' + ' changed -> ' + '\'' + drive_choice + '\'')
			current_iso_path = current_iso_path.replace(self.drive_system_array[0], drive_choice)
			self.update_iso_path_entry_field(current_iso_path)
			self.drive_system_array[0] = drive_choice

		# Replace current system
		if system_choice not in current_iso_path:
			print('DEBUG system_choice not in current_iso_path')
			print('DEBUG ' + '\'' + self.drive_system_array[1] + '\'' + ' changed -> ' + '\'' + system_choice + '\'')
			current_iso_path = current_iso_path.replace(self.drive_system_array[1], system_choice)
			self.update_iso_path_entry_field(current_iso_path)
			self.drive_system_array[1] = system_choice

	# Dynamic update of the pkg path for showing fetched images
	def dynamic_game_build_path(self):
		AppPaths.game_work_dir = os.path.join(self.gamelist.get_selected_build_dir_path(), 'work_dir')
		build_dir_pkg_path = os.path.join(AppPaths.game_work_dir, 'pkg')
		if os.path.exists(build_dir_pkg_path):
			# update images
			self.init_draw_images_on_canvas(self.main, pkg_build_path=build_dir_pkg_path)

	# Dynamic update of the 'entry_field_filename' into the 'entry_field_iso_path'
	def dynamic_filename_to_path(self, event):
		drive = ''
		system = ''
		filename = event.widget.get()

		if self.drive_system_array[0] is not None:
			drive = '/' + self.drive_system_array[0] + '/'
		if self.drive_system_array[1] is not None:
			system = '/' + self.drive_system_array[1] + '/'

		iso_path = drive + system + filename
		iso_path = iso_path.replace('//', '/')

		self.entry_field_iso_path.xview_moveto(1)
		self.update_iso_path_entry_field(iso_path)


	def update_iso_path_entry_field(self, iso_path):
		self.entry_field_iso_path.config(state='normal')
		self.entry_field_iso_path.delete(0, END)
		self.entry_field_iso_path.insert(0, iso_path)
		self.entry_field_iso_path.config(state='readonly')

	# Dynamic update of the game title on to the PIC1 image
	def dynamic_title_to_pic1(self, event):
		self.dynamic_game_build_path()
		tmp_img = copy.copy(self.image_pic1)
		# self, image, text, text_x, text_y, text_size, text_outline, text_color,
		self.draw_text_on_image_w_shadow(tmp_img, event.widget.get(), 760, 487, 32, 2, 'white', 'black')
		self.image_pic1_w_title = copy.copy(tmp_img)
		tmp_img = tmp_img.resize((int(1280 * scaling), int(720 * scaling)), Image.ANTIALIAS)
		self.photo_image_pic1_xmb = PhotoImage(tmp_img)
		self.button_pic1.config(image=self.photo_image_pic1_xmb)

	def image_replace_browser(self, main):
		image = askopenfile(mode='rb', title='Browse an image', filetypes=[('PNG images', '.PNG')])
		if image is not None:
			img_to_be_changed = None
			print('DEBUG image content:' + image.name)

			# Clear and replace image
			if 'icon0' in image.name.lower():
				self.image_icon0 = Image.open(image)
				self.image_icon0_ref = copy.copy(self.image_icon0)
				img_to_be_changed = 'icon0'
			elif 'pic1' in image.name.lower():
				self.image_pic1 = Image.open(image)
				self.image_pic1_ref = Image.open(image)
				img_to_be_changed = 'pic1'

			# # re-draw work_dir image on canvas
			self.init_draw_images_on_canvas(main, img_to_be_changed=img_to_be_changed)

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
		if len(P) > 0:
			P = P.upper()
			P = P.replace('-', '')
			P = re.sub(r'[^a-zA-Z0-9 -]', '', P)

			self.entry_field_title_id.delete(0, END)
			self.entry_field_title_id.insert(0, P[0:self.title_id_maxlength])
			main_window.after_idle(lambda: self.entry_field_title_id.config(validate='key'))
			return True
		else:
			return False

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

		if str(tmp_name).endswith('.iso') or str(tmp_name).endswith('.bin') and len(tmp_name) > 4:
			main_window.focus()
			return True


		elif str(tmp_name).endswith('.iso') or str(tmp_name).endswith('.bin'):
			self.filename_error_msg = 'The image file must have a name'
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

	def validate_fields(self):
		# do stuff
		if self.validate_title_id_on_save():
			print('DEBUG: Title_id: OK')
		else:
			return False
		if self.validate_title_on_save():
			print('DEBUG: Title: OK')
		else:
			return False
		if self.validate_filename_on_save():
			print('DEBUG: Title_id: OK')
		else:
			return False

		return True

	def save_work_dir(self):
		if self.validate_fields():
			self.image_icon0.save(os.path.join(self.wcm_pkg_dir, 'ICON0.PNG'))
			self.image_pic0.save(os.path.join(self.wcm_pkg_dir, 'PIC0.PNG'))
			self.image_pic1.save(os.path.join(self.wcm_pkg_dir, 'PIC1.PNG'))

			self.save_preview_image()
			self.save_pkg_info_to_json()

			return True
		else:
			return False

	def copytree(self, src, dst, symlinks=False, ignore=None):
		if not os.path.exists(dst):
			os.makedirs(dst)
			shutil.copystat(src, dst)
		lst = os.listdir(src)
		if ignore:
			excl = ignore(src, lst)
			lst = [x for x in lst if x not in excl]
		for item in lst:
			s = os.path.join(src, item)
			d = os.path.join(dst, item)
			if symlinks and os.path.islink(s):
				if os.path.lexists(d):
					os.remove(d)
				os.symlink(os.readlink(s), d)
				try:
					st = os.lstat(s)
					mode = stat.S_IMODE(st.st_mode)
					os.lchmod(d, mode)
				except:
					pass  # lchmod not available
			elif os.path.isdir(s):
				self.copytree(s, d, symlinks, ignore)
			else:
				shutil.copy2(s, d)

	def on_build_button(self):
		if os.path.isdir(os.path.join(AppPaths.resources, 'pkg')):
			shutil.rmtree(os.path.join(AppPaths.resources, 'pkg'))
		self.copytree(os.path.join(AppPaths.util_resources, 'pkg_dir_bak'), os.path.join(AppPaths.resources, 'pkg'))

		if self.save_work_dir():
			title_id = str(self.entry_field_title_id.get()).replace('-', '')
			filename = str(self.entry_field_filename.get())
			game_pkg_dir = os.path.join(AppPaths.game_work_dir, 'pkg')

			if not os.path.exists(self.pkg_dir):
				os.makedirs(self.pkg_dir)

			if os.path.isfile(os.path.join(game_pkg_dir, 'ICON0.PNG')):
				shutil.copyfile(os.path.join(game_pkg_dir, 'ICON0.PNG'), os.path.join(self.pkg_dir, 'ICON0.PNG'))

			if os.path.isfile(os.path.join(game_pkg_dir, 'PIC0.PNG')):
				shutil.copyfile(os.path.join(game_pkg_dir, 'PIC0.PNG'), os.path.join(self.pkg_dir, 'PIC0.PNG'))

			if os.path.isfile(os.path.join(game_pkg_dir, 'PIC1.PNG')):
				shutil.copyfile(os.path.join(game_pkg_dir, 'PIC1.PNG'), os.path.join(self.pkg_dir, 'PIC1.PNG'))

			# builds pkg and reads the pkg filename
			webman_pkg = Webman_PKG()

			pkg_name = webman_pkg.build()
			if pkg_name is not None:
				# making sure default work_dir and pkg directories exists
				if not os.path.exists(game_pkg_dir):
					os.makedirs(game_pkg_dir)

				# saving the build content in the game build folder
				self.copytree(self.pkg_dir, game_pkg_dir)

				# clean up the temp work dir
				if os.path.isdir(AppPaths.game_work_dir):
					self.init_wcm_work_dir()
					import tkMessageBox
					def popup():
						msgBox = tkMessageBox.showinfo("Build status", "Build successful!")
					popup()

					# open builds folder in windows explorer
					if 'win' in sys.platform:
						print('DEBUG opening folder: ' + os.path.join(AppPaths.game_work_dir, '..'))
						try:
							os.startfile(os.path.join(AppPaths.game_work_dir, '../'))
						except:
							print('ERROR: Could open the pkg build dir from Windows explorer')

			else:
				import tkMessageBox
				tkMessageBox.showinfo("Build status", "Build failed!")



	def on_ftp_fetch_button(self):
		# save the ps3-ip field to config file
		self.save_ps3_ip_on_fetch()
		ftp_game_list = FtpGameList()
		ftp_game_list.execute()

		self.on_game_list_refresh()


	def save_ps3_ip_on_fetch(self):
		with open(self.ftp_settings_path, 'r') as settings_file:
			json_settings_data = json.load(settings_file)
			json_settings_data['ps3_lan_ip'] = str(self.entry_field_ftp_ip.get())
			json_settings_data['ftp_lan_ip'] = str(self.entry_field_ftp_ip.get())
			json_settings_data['ftp_user'] = str(self.entry_field_ftp_user.get())
			json_settings_data['ftp_password'] = str(self.entry_field_ftp_pass.get())
			settings_file.close()
		# save to file
		with open(self.ftp_settings_path, 'w') as save_settings_file:
			new_json_data = json.dumps(json_settings_data, indent=4, separators=(",", ":"))
			save_settings_file.write(new_json_data)
			save_settings_file.close()



	def save_preview_image(self):
		# making a preview print of the game canvas
		if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC1.PNG')):
			pic1_img = Image.open(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC1.PNG')).convert("RGBA")
			preview_img = Image.open(os.path.join(AppPaths.resources, 'images', 'pkg', 'default', 'PIC1.PNG')).convert("RGBA")
			preview_img.paste(pic1_img, (0, 0), pic1_img)
		else:
			preview_img = Image.open(os.path.join(AppPaths.resources, 'images', 'pkg', 'default', 'PIC1.PNG')).convert("RGBA")

		if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC0.PNG')):
			pic0_img = Image.open(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC0.PNG')).convert("RGBA")
			preview_img.paste(pic0_img, (self.pic0_x_pos, self.pic0_y_pos), pic0_img)

		if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'ICON0.PNG')):
			icon0_img = Image.open(os.path.join(AppPaths.game_work_dir, 'pkg', 'ICON0.PNG')).convert("RGBA")
			preview_img.paste(icon0_img, (self.icon0_x_pos, self.icon0_y_pos), icon0_img)

		# print('DEBUG: ' + os.path.dirname(__file__))
		xmb_img_dir = os.path.join(ImagePaths.xmb, 'XMB_icons.png')
		xmb_img = Image.open(xmb_img_dir).convert("RGBA")

		self.draw_text_on_image_w_shadow(preview_img, "11/11/2006 00:00", 760, 522, 20, 1, 'white', 'black')
		self.draw_text_on_image_w_shadow(preview_img, str(self.entry_field_title.get()), 760, 487, 32, 2, 'white',
										 'black')


		preview_img.paste(xmb_img, (0, 0), xmb_img)

		preview_img.save(os.path.join(AppPaths.game_work_dir, '..', 'preview.png'))

	def on_game_list_refresh(self):
		self.create_list_combo_box(self.list_filter_platform)

	def save_pkg_info_to_json(self):
		with open(os.path.join(AppPaths.util_resources, 'pkg.json.BAK')) as f:
			json_data = json.load(f)

		try:
			json_data['title'] = str(self.entry_field_title.get())
			json_data['title_id'] = self.entry_field_title_id.get()
			json_data['content_id'] = 'UP0001-' + self.entry_field_title_id.get() + '_00-0000000000000000'
			json_data['iso_filepath'] = str(self.entry_field_iso_path.get())

			pkg_json_path = os.path.join(AppPaths.game_work_dir, 'pkg.json')
			# if (os.path.isfile(pkg_json_path)):
			# 	os.remove(pkg_json_path)
			newFile = open(pkg_json_path, "w")
			json_text = json.dumps(json_data, indent=4, separators=(",", ":"))
			newFile.write(json_text)

		except ValueError as e:
			print("ERROR: File write error or 'PKGLAUNCH'/title-_d not found.")
			print(e.message)

class CreateToolTip(object):
	"""
    create a tooltip for a given widget
    """
	def __init__(self, widget, text='widget info'):
		self.waittime = 350     #miliseconds
		self.wraplength = 180   #pixels
		self.widget = widget
		self.text = text
		self.widget.bind("<Enter>", self.enter)
		self.widget.bind("<Leave>", self.leave)
		self.widget.bind("<ButtonPress>", self.leave)
		self.id = None
		self.tw = None

	def enter(self, event=None):
		self.schedule()

	def leave(self, event=None):
		self.unschedule()
		self.hidetip()

	def schedule(self):
		self.unschedule()
		self.id = self.widget.after(self.waittime, self.showtip)

	def unschedule(self):
		id = self.id
		self.id = None
		if id:
			self.widget.after_cancel(id)

	def showtip(self, event=None):
		import Tkinter as tk
		x = y = 0
		x, y, cx, cy = self.widget.bbox("insert")
		x += self.widget.winfo_rootx() + 25
		y += self.widget.winfo_rooty() + 20
		# creates a toplevel window
		self.tw = tk.Toplevel(self.widget)
		# Leaves only the label and removes the app window
		self.tw.wm_overrideredirect(True)
		self.tw.wm_geometry("+%d+%d" % (x, y))
		label = tk.Label(self.tw, text=self.text, justify='left',
						 background="#ffffff", relief='solid', borderwidth=1,
						 wraplength = self.wraplength)
		label.pack(ipadx=1)

	def hidetip(self):
		tw = self.tw
		self.tw= None
		if tw:
			tw.destroy()

# setup properties
main_window = Tk()
main_window.geometry("+%d+%d" % (0, 0))
main_window.title('Webman Classics Maker')

# icon upper left corner
if "linux" in sys.platform:
	print('DEBUG Running Linux')
	main_window.iconbitmap('@' + os.path.join(ImagePaths.misc, 'webman_icon.xbm'))
elif 'win' in sys.platform:
	print('DEBUG Running Windows')
	main_window.iconbitmap(os.path.join(ImagePaths.misc, 'webman.ico'))

else:
	print('DEBUG Running ' + str(sys.platform))

scaling = 720.0 / 1080.0
canvas_width = int(1920 * scaling)
canvas_height = int(1080 * scaling)
main_window_width = int(1920 * scaling)
main_window_height = int(1080 * scaling)

Main()
main_window.mainloop()
