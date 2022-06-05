#!/usr/bin/env python3
import copy
import json
import os
import sys
import shutil
import traceback
import urllib.parse
from urllib.request import urlopen

# sudo apt-get install python3-tk
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile

from resources.tools.util_scripts.global_paths import AppPaths
from resources.tools.util_scripts.global_paths import ImagePaths
from resources.tools.util_scripts.global_paths import GlobalVar
from resources.tools.util_scripts.global_paths import FtpSettings
from resources.tools.util_scripts.global_paths import GameListData
from resources.tools.util_scripts.global_paths import GlobalDef
from resources.tools.util_scripts.build_all_scripts import Webman_PKG
from resources.tools.util_scripts.wcm_gui.drop_down import DriveDropdown, PlatformDropdown
from resources.tools.util_scripts.wcm_gui.ftp_game_data_fetcher import FtpGameList
from resources.tools.util_scripts.wcm_gui.game_listbox import Gamelist

if getattr(sys, 'frozen', False):
    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'resources', 'tools', 'util_scripts'))
    sys.path.append(os.path.join(os.path.dirname(sys.executable), 'resources', 'tools', 'util_scripts', 'wcm_gui'))
else:
    # running webman_classics_maker.py from root
    app_full_path = os.path.realpath(__file__)
    application_path = os.path.dirname(app_full_path)
    sys.path.append(os.path.join(application_path, 'resources', 'tools', 'util_scripts'))
    sys.path.append(os.path.join(application_path, 'resources', 'tools', 'util_scripts', 'wcm_gui'))

# pip install Pillow
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageTk import PhotoImage


def __init_pkg_build_dir__():
    if os.path.isdir(AppPaths.pkg):
        if 'webman-classics-maker' in AppPaths.pkg.lower():
            shutil.rmtree(AppPaths.pkg)
    if not os.path.isdir(AppPaths.pkg):
        os.makedirs(AppPaths.pkg)
    GlobalDef().copytree(os.path.join(AppPaths.util_resources, 'pkg_dir_bak'),
                         os.path.join(AppPaths.resources, 'pkg'))


def __init_images__(self):

    # ui images
    self.image_xmb_icons = Image.open(os.path.join(ImagePaths.xmb, 'XMB_icons.png'))
    self.ps3_gametype_logo = Image.open(os.path.join(ImagePaths.xmb, 'ps3_type_logo.png'))

    # # button images
    # self.images_logo_drive = []
    # self.images_logo_drive.append(PhotoImage(self.make_button_smallest('HDD', font='conthrax-sb.ttf', x=-1, y=-2)))
    # self.images_logo_drive.append(PhotoImage(self.make_button_smallest('USB', font='conthrax-sb.ttf', x=-1, y=-2)))
    #
    # self.images_logo_system = []
    # self.images_logo_system.append(PhotoImage(self.make_button_smallest('PSP', font='conthrax-sb.ttf', x=-1, y=-2)))
    # self.images_logo_system.append(PhotoImage(self.make_button_smallest('PSX', font='conthrax-sb.ttf', x=-1, y=-2)))
    # self.images_logo_system.append(PhotoImage(self.make_button_smallest('PS2', font='conthrax-sb.ttf', x=-1, y=-2)))
    # self.images_logo_system.append(PhotoImage(self.make_button_smallest('PS3', font='conthrax-sb.ttf', x=-1, y=-2)))
    #
    # self.images_function_button = []
    # self.images_function_button.append(PhotoImage(self.make_smal_button('Build', font='arial.ttf', x=3, y=0)))
    # self.images_function_button.append(PhotoImage(self.make_smal_button('Add', font='arial.ttf', x=3, y=0)))
    # self.images_function_button.append(PhotoImage(self.make_smal_button('Save', font='arial.ttf', x=3, y=0)))
    # # self.images_function_button.append(PhotoImage(self.small_button_maker('Quit', font='arial.ttf', x=3, y=0)))
    # # self.images_function_button.append(PhotoImage(self.small_button_maker('Change', font='arial.ttf', x=-3, y=0)))
    #
    # self.images_gamelist_button = []
    # self.images_gamelist_button.append(PhotoImage(self.make_smal_button('Fetch', font='arial.ttf', x=3, y=0)))
    # self.images_gamelist_button.append(PhotoImage(self.make_smal_button('Refresh', font='arial.ttf', x=-1, y=0)))

    self.hdd_button_image = PhotoImage(self.make_button_smallest('HDD', font='conthrax-sb.ttf', x=-1, y=-2))
    self.usb_button_image = PhotoImage(self.make_button_smallest('USB', font='conthrax-sb.ttf', x=-1, y=-2))
    self.psp_button_image = PhotoImage(self.make_button_smallest('PSP', font='conthrax-sb.ttf', x=-1, y=-2))
    self.psx_button_image = PhotoImage(self.make_button_smallest('PSX', font='conthrax-sb.ttf', x=-1, y=-2))
    self.ps2_button_image = PhotoImage(self.make_button_smallest('PS2', font='conthrax-sb.ttf', x=-1, y=-2))
    self.ps3_button_image = PhotoImage(self.make_button_smallest('PS3', font='conthrax-sb.ttf', x=-1, y=-2))
    self.build_button_image = PhotoImage(self.make_smal_button('Build', font='arial.ttf', x=3, y=0))
    self.add_button_image = PhotoImage(self.make_smal_button('Add', font='arial.ttf', x=3, y=0))
    self.save_button_image = PhotoImage(self.make_smal_button('Save', font='arial.ttf', x=3, y=0))
    # self.quit_button_image = PhotoImage(self.make_smal_button('Quit', font='arial.ttf', x=3, y=0))
    # self.change_button_image = PhotoImage(self.make_smal_button('Change', font='arial.ttf', x=-3, y=0))
    self.fetch_button_image = PhotoImage(self.make_smal_button('Fetch', font='arial.ttf', x=3, y=0))
    self.refresh_button_image = PhotoImage(self.make_smal_button('Refresh', font='arial.ttf', x=-1, y=0))


    # pkg images
    self.pkg_icon0 = None
    self.pkg_pic0 = None
    self.pkg_pic1 = None

    icon0_filename = 'ICON0.PNG'
    pic0_filename = 'PIC0.PNG'
    pic1_filename = 'PIC1.PNG'

    self.image_icon0 = self.load_default_pkg_images(icon0_filename)
    self.image_icon0_ref = copy.copy(self.image_icon0)

    self.image_pic0 = self.load_default_pkg_images(pic0_filename)
    self.image_pic0_ref = copy.copy(self.image_pic0)

    self.image_pic1 = self.load_default_pkg_images(pic1_filename)
    self.image_pic1_ref = copy.copy(self.image_pic1)
    self.image_pic1_w_title = copy.copy(self.image_pic1)

    # ui background image
    self.background_images = []
    self.load_backgrounds()
    self.canvas_image_number = 0
    self.current_img = self.background_images[self.canvas_image_number]
    self.current_background = PhotoImage(self.current_img)


def __init_wcm_work_dir__(self):
    # clean and init wcm_work_dir in startup
    if os.path.isdir(AppPaths.wcm_work_dir):
        if 'webman-classics-maker' in AppPaths.wcm_work_dir.lower():
            shutil.rmtree(AppPaths.wcm_work_dir)
    if not os.path.isdir(os.path.join(AppPaths.wcm_work_dir, 'pkg')):
        os.makedirs(os.path.join(AppPaths.wcm_work_dir, 'pkg'))
        __init_images__(self)


def get_ftp_ip_from_config():
    return FtpSettings.ps3_lan_ip


def get_ftp_user_from_config():
    return FtpSettings.ftp_user


def get_ftp_pass_from_config():
    return FtpSettings.ftp_password


def __init_buttons__(self):
    # buttons
    self.button_icon0	 = None
    self.button_pic0	 = None
    self.button_pic1	 = None

    self.button_HDD	 	 = None
    self.button_USB	 	 = None

    self.button_PSP 	 = None
    self.button_PSX 	 = None
    self.button_PS2 	 = None
    self.button_PS3 	 = None

    self.build_button	 = None
    self.fetch_button	 = None
    self.refresh_button	 = None

    self.drive_dropdown	 = None
    self.platform_dropdown = None

    # text tooltip messages
    self.USB_BUTTON_TOOLTIP_MSG = "Toggle USB port (0-3)"

    self.BUILD_BUTTON_TOOLTIP_MSG = "Save & Build pkg"
    self.SAVE_BUTTON_TOOLTIP_MSG = "Save data"
    self.FETCH_BUTTON_TOOLTIP_MSG = "Fetch gamelist and images over FTP"
    self.REFRESH_BUTTON_TOOLTIP_MSG = "Refresh gamelist from disk"

    self.ICON0_TOOLTIP_MSG = "Click to replace ICON0"
    self.PIC0_TOOLTIP_MSG = "Click to replace  PIC0"
    self.PIC1_TOOLTIP_MSG = "Click to replace  PIC1"


class Main:
    def __init__(self):
        self.main = main_window

        # window metrics
        self.scaling = 720.0 / 1080.0
        self.canvas_height = int(1080 * self.scaling)
        self.canvas_width = int(1920 * self.scaling)

        self.main_window_width = int(1920 * self.scaling)
        self.main_window_height = int(1080 * self.scaling)

        self.main_offset_x_pos = 1450
        self.main_offset_y_pos = 50

        # common paths
        self.WCM_BASE_PATH 		= AppPaths.wcm_gui
        self.pkg_dir 			= AppPaths.pkg
        self.wcm_work_dir 		= AppPaths.wcm_work_dir
        self.wcm_pkg_dir 		= os.path.join(self.wcm_work_dir, 'pkg')
        self.builds_path 		= AppPaths.builds
        self.ftp_settings_path 	= os.path.join(AppPaths.settings, 'ftp_settings.cfg')
        self.fonts_path 		= AppPaths.fonts

        self.vcmd = self.main.register(self.dynamic_validate_title_id)
        self.vcmd2 = self.main.register(self.dynamic_validate_title_id)
        self.title_id_maxlength = len('PKGLAUNCH')
        self.tmp_title_id = ''
        self.global_platform_paths = GlobalVar.platform_paths

        self.drive_system_path_array = ['drive', 'system', 'path']
        self.entry_field_iso_path = None
        self.usb_port_number = 0

        # gui assets
        __init_images__(self)

        __init_buttons__(self)

        # canvas as background_image
        self.canvas = Canvas(self.main,
                             width=self.canvas_width,
                             height=self.canvas_height,
                             borderwidth=0,
                             highlightthickness=0)

        self.canvas.pack(fill=BOTH, expand=YES)
        self.image_on_canvas = self.canvas.create_image(0, 0, anchor=NW, image=self.current_background)



        self.init_default_view(self.main)
        self.draw_background_on_canvas()

        # init gamelist and filters
        self.list_filter_drive = 'ALL'
        self.list_filter_platform = 'ALL'

        self.game_list = Gamelist(self)
        self.game_list_box = self.game_list.get_listbox()
        self.create_dropdowns()

        self.drive_dropdown = DriveDropdown(self.canvas, self.game_list_box).get_box()
        self.platform_dropdown = PlatformDropdown(self.canvas, self.game_list_box).get_box()



    def create_dropdowns(self):
        # ensure drive_dropdown into the listbox
        if self.drive_dropdown is None:
            self.drive_dropdown = DriveDropdown(self.canvas, self.game_list_box).get_box()
        self.drive_dropdown.bind("<<ComboboxSelected>>", self.dropdown_filter_callback)

        # ensure platform_dropdown into the listbox
        if self.platform_dropdown is None:
            self.platform_dropdown = PlatformDropdown(self.canvas, self.game_list_box).get_box()
        self.platform_dropdown.bind("<<ComboboxSelected>>", self.dropdown_filter_callback)

    def dropdown_filter_callback(self, event):
        dropdown_name = str(event.widget).split(".")[-1]
        if dropdown_name == 'drive_dropdown':
            self.list_filter_drive = event.widget.get()
            self.drive_dropdown.set(self.list_filter_drive)
        elif dropdown_name == 'platform_dropdown':
            self.list_filter_platform = event.widget.get()
            self.platform_dropdown.set(self.list_filter_platform)
            # NTFS can only be used combined with HDD0
            if 'NTFS' == self.list_filter_platform:
                self.list_filter_drive = 'HDD0'
                self.drive_dropdown.set('HDD0')

        self.create_dropdowns()
        self.game_list_box.focus()

    def make_button_smallest(self, text, **args):
        font = None
        x = None
        y = None
        icon_bg_img = Image.new('RGB', (44, 15), color='black')
        for key, value in args.items():
            if 'font' == key:
                font = value
            elif 'x' == key:
                x = value
            elif 'y' == key:
                y = value
            elif 'width' == key:
                width = value
            elif 'height' == key:
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

    def make_smal_button(self, text, **args):
        font = None
        x = None
        y = None
        icon_bg_img = Image.new('RGB', (50, 20), color='black')
        for key, value in args.items():
            if 'font' == key:
                font = value
            elif 'x' == key:
                x = value
            elif 'y' == key:
                y = value
            elif 'width' == key:
                width = value
            elif 'height' == key:
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



    def load_default_pkg_images(self, filename):
        default_pkg_img_dir = os.path.join(ImagePaths.pkg, 'default')
        return Image.open(os.path.join(default_pkg_img_dir, filename)).convert("RGBA")

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
        self.current_img = self.current_img.resize((int(1920 * self.scaling), int(1080 * self.scaling)), Image.Resampling.LANCZOS)

        self.tv_frame = Image.open(
            os.path.join(ImagePaths.misc, 'tv_frame_1080_ps3_3.png')).resize(
            (int(1990 * self.scaling), int(1327 * self.scaling)), Image.Resampling.LANCZOS)
        self.current_img.paste(self.tv_frame, (int(45 * self.scaling), int(143 * self.scaling)), self.tv_frame)

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

        # gamelist and entry fields
        self.entry_field_title_id 	= Entry(main, validate='key', validatecommand=(self.vcmd, '%P'))
        self.entry_field_title 		= Entry(main)
        self.entry_field_filename 	= Entry(main)
        self.entry_field_iso_path 	= Entry(main, state='readonly')
        # not visible in GUI
        self.entry_field_platform   = Entry(main)

        ##########################################################################
        # Adding an on_change-listener on 'entry_field_title'
        self.generate_on_change(self.entry_field_title)
        self.entry_field_title.bind('<<Change>>', self.dynamic_title_to_pic1)
        ###########################################################################
        # Adding an on_change-listener on 'entry_field_filename'
        self.generate_on_change(self.entry_field_filename)
        self.entry_field_filename.bind('<<Change>>', self.dynamic_filename_and_path)
        ###########################################################################

        self.entry_field_ftp_ip = Entry(main)
        self.entry_field_ftp_ip.insert(0, get_ftp_ip_from_config())

        self.entry_field_ftp_user = Entry(main)
        self.entry_field_ftp_user.insert(0, get_ftp_user_from_config())

        self.entry_field_ftp_pass = Entry(main)
        self.entry_field_ftp_pass.insert(0, get_ftp_pass_from_config())

        # system choice buttons
        self.selection_drive_list = ['dev_hdd0',
                                     'dev_usb000', 'dev_usb001', 'dev_usb002',
                                     'dev_usb003']  # usb port 'x' should be selected through a list
        self.selection_system_list = ['PSPISO', 'PSXISO', 'PS2ISO', 'PS3ISO']
        self.drive_path = self.selection_drive_list[0]  # drive should be toggled by buttons

        self.button_HDD = Button(main,
                                 image=self.hdd_button_image,
                                 borderwidth=1,
                                 command=lambda: self.on_drive_button(self.selection_drive_list[0]))

        self.button_USB = Button(main,
                                 image=self.usb_button_image,
                                 borderwidth=1,
                                 command=lambda:
                                 self.on_drive_button(self.selection_drive_list[self.usb_port_number + 1]))

        self.button_PSP = Button(main,
                                 image=self.psp_button_image,
                                 borderwidth=1,
                                 command=lambda:
                                 self.on_system_button(self.drive_system_path_array[0], self.selection_system_list[0]))

        self.button_PSX = Button(main,
                                 image=self.psx_button_image,
                                 borderwidth=1,
                                 command=lambda:
                                 self.on_system_button(self.drive_system_path_array[0], self.selection_system_list[1]))

        self.button_PS2 = Button(main,
                                 image=self.ps2_button_image,
                                 borderwidth=1,
                                 command=lambda:
                                 self.on_system_button(self.drive_system_path_array[0], self.selection_system_list[2]))

        self.button_PS3 = Button(main,
                                 image=self.ps3_button_image,
                                 borderwidth=1,
                                 command=lambda:
                                 self.on_system_button(self.drive_system_path_array[0], self.selection_system_list[3]))



        # build, save and remove buttons
        self.build_button = Button(main,
                                   image=self.build_button_image,
                                   borderwidth=0,
                                   command=self.on_build_button,
                                   bg="#FBFCFB")

        self.save_button = Button(main,
                                  image=self.save_button_image,
                                  borderwidth=0,
                                  command=self.on_save_button,
                                  bg="#FBFCFB")

        # ftp list buttons
        self.fetch_button = Button(main,
                                   image=self.fetch_button_image,
                                   borderwidth=0,
                                   command=self.on_ftp_fetch_button,
                                   bg="#FBFCFB")


        self.refresh_button = Button(main,
                                     image=self.refresh_button_image,
                                     borderwidth=0,
                                     command=self.on_game_list_refresh,
                                     bg="#FBFCFB")

        # button tooltips
        CreateToolTip(self.button_USB, self.USB_BUTTON_TOOLTIP_MSG)

        CreateToolTip(self.build_button, self.BUILD_BUTTON_TOOLTIP_MSG)
        CreateToolTip(self.save_button, self.SAVE_BUTTON_TOOLTIP_MSG)

        CreateToolTip(self.fetch_button, self.FETCH_BUTTON_TOOLTIP_MSG)
        CreateToolTip(self.refresh_button, self.REFRESH_BUTTON_TOOLTIP_MSG)

        # Entry field placements
        entry_field_width = 200
        self.entry_field_title_id.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * self.scaling),
                                        y=int(self.title_id_text_y_pos * self.scaling),
                                        width=entry_field_width)

        self.entry_field_title.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * self.scaling),
                                     y=int(self.title_text_y_pos * self.scaling),
                                     width=entry_field_width)

        self.entry_field_filename.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * self.scaling),
                                        y=int(self.filename_text_y_pos * self.scaling),
                                        width=entry_field_width)

        self.entry_field_iso_path.place(x=int((self.text_box_spacing + self.main_offset_x_pos) * self.scaling),
                                        y=int(self.iso_path_text_y_pos * self.scaling),
                                        width=entry_field_width)

        self.entry_field_ftp_ip.place(x=int((self.main_offset_x_pos + 90) * self.scaling),
                                      y=int((self.main_offset_y_pos + 815) * self.scaling),
                                      width=90)

        self.entry_field_ftp_user.place(x=int((self.main_offset_x_pos + 320) * self.scaling),
                                        y=int((self.main_offset_y_pos + 815) * self.scaling),
                                        width=60)

        self.entry_field_ftp_pass.place(x=int((self.main_offset_x_pos + 320) * self.scaling),
                                        y=int((self.main_offset_y_pos + 850) * self.scaling),
                                        width=60)

        # Button placements
        self.button_HDD.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 0 * 75) * self.scaling),
                              y=int(self.device_text_y_pos * self.scaling))

        self.button_USB.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 1 * 75) * self.scaling),
                              y=int(self.device_text_y_pos * self.scaling))

        self.button_PSP.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 0 * 75) * self.scaling),
                              y=int(self.type_text_y_pos * self.scaling))

        self.button_PSX.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 1 * 75) * self.scaling),
                              y=int(self.type_text_y_pos * self.scaling))

        self.button_PS2.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 2 * 75) * self.scaling),
                              y=int(self.type_text_y_pos * self.scaling))

        self.button_PS3.place(x=int((self.text_box_spacing + self.main_offset_x_pos + 3 * 75) * self.scaling),
                              y=int(self.type_text_y_pos * self.scaling))

        # draws ICON0, PIC0 and PIC1 on the canvas
        self.init_draw_images_on_canvas(main)

        self.button_spacing = 70


        # self.save_button.place(
        #     x=int((self.text_box_spacing + self.main_offset_x_pos) * scaling),
        #     y=int((self.iso_path_text_y_pos + 40) * scaling))


        self.build_button.place(
            x=int((self.text_box_spacing + self.main_offset_x_pos + 0 * 85) * self.scaling),
            y=int((self.iso_path_text_y_pos + 40) * self.scaling))

        self.fetch_button.place(
            x=int((self.main_offset_x_pos) * self.scaling),
            y=int((self.main_offset_y_pos + 855) * self.scaling))

        self.save_button.place(
            x=int((self.text_box_spacing + self.main_offset_x_pos + 1 * 85) * self.scaling),
            y=int((self.iso_path_text_y_pos + 40) * self.scaling))

        self.refresh_button.place(
            x=int((self.main_offset_x_pos + 80) * self.scaling),
            y=int((self.main_offset_y_pos + 855) * self.scaling))



    def init_draw_images_on_canvas(self, main, *args, **kwargs):
        tmp_image_icon0 = None
        img_to_be_changed = kwargs.get('img_to_be_changed', None)
        pkg_build_path = kwargs.get('pkg_build_path', None)
        default_img_path = os.path.join(AppPaths.resources, 'images', 'pkg', 'default')

        pic1_changed = False
        pic0_changed = False
        icon0_changed = False

        # TODO image replace browser: missing the title text!
        print('image to be changed: ' + str(img_to_be_changed))
        if img_to_be_changed not in {'', None}:

            if img_to_be_changed.lower() == 'pic1':
                pic1_changed = True
                self.draw_text_on_image_w_shadow(self.image_pic1, self.entry_field_title.get(), 745, 457, 32, 2, 'white', 'black')

                self.photo_image_pic1_xmb = PhotoImage(
                    self.image_pic1.resize((int(1280 * self.scaling), int(720 * self.scaling)), Image.Resampling.LANCZOS))

                self.button_pic1.config(image=self.photo_image_pic1_xmb)
                self.image_pic0 = self.image_pic0_ref
                self.image_icon0 = self.image_icon0_ref

            elif img_to_be_changed.lower() == 'pic0':
                self.image_pic0 = self.image_pic0_ref
                pic0_changed = True


        # check if xmb_icons needs to be re-drawn
        elif pkg_build_path not in {'', None}:
            if os.path.exists(pkg_build_path):
                # draw PIC1 from pkg_dir and then xmb icons and system logo onto the pkg  background
                if os.path.isfile(os.path.join(pkg_build_path, 'ICON0.PNG')):
                    icon0_changed = True
                    self.image_icon0 = Image.open(os.path.join(pkg_build_path, 'ICON0.PNG')).convert("RGBA")

                if os.path.isfile(os.path.join(pkg_build_path, 'PIC0.PNG')):
                    pic0_changed = True
                    self.image_pic0 = Image.open(os.path.join(pkg_build_path, 'PIC0.PNG')).convert("RGBA")

                if os.path.isfile(os.path.join(pkg_build_path, 'PIC1.PNG')):
                    self.image_pic1 = Image.open(os.path.join(pkg_build_path, 'PIC1.PNG')).convert("RGBA")
                    self.image_pic1_ref = Image.open(os.path.join(pkg_build_path, 'PIC1.PNG')).convert("RGBA")
                    pic1_changed = True

        else:
            # extract the platform name by using the path
            platform = ''
            if self.entry_field_platform == 'NTFS':
                match = re.search('(?<=\[).*?(?=\])', str(self.entry_field_filename.get()))
                if match is not None:
                    donor_platform = filter(lambda x: match.group() in x[0], self.global_platform_paths)
                    if donor_platform:
                        platform = list(donor_platform)[0][1]

            self.image_icon0 = Image.open(os.path.join(default_img_path, platform, 'ICON0.PNG')).convert("RGBA")
            self.image_icon0_ref = Image.open(os.path.join(default_img_path, 'ICON0.PNG')).convert("RGBA")

            self.image_pic0 = Image.open(os.path.join(default_img_path, 'PIC0.PNG')).convert("RGBA")
            self.image_pic0_ref = Image.open(os.path.join(default_img_path, 'PIC0.PNG')).convert("RGBA")

            self.image_pic1 = Image.open(os.path.join(default_img_path, 'PIC1.PNG')).convert("RGBA")
            self.image_pic1_ref = Image.open(os.path.join(default_img_path, 'PIC1.PNG')).convert("RGBA")
            pic1_changed = True


        if pic1_changed:
            # draw xmb icons and system logo onto the background
            self.image_pic1.paste(self.image_xmb_icons, (0, 0), self.image_xmb_icons)
            self.image_pic0.paste(self.ps3_gametype_logo, (1180, 525), self.ps3_gametype_logo)

        # ICON0 is mandatory
        if not os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'ICON.PNG')):
            tmp_image_icon0 = Image.open(os.path.join(default_img_path, 'ICON0.PNG')).convert("RGBA")
            icon0_changed = True


        if pic1_changed or icon0_changed:
            # crop and blend ICON0 to the background
            tmp_icon0_bg = copy.copy(self.image_pic1_ref)
            tmp_icon0_bg.paste(self.image_icon0.convert("RGBA"), (self.icon0_x_pos, self.icon0_y_pos), self.image_icon0.convert("RGBA"))
            # Image.crop((left, top, right, bottom))
            tmp_image_icon0 = tmp_icon0_bg.crop((self.icon0_x_pos, self.icon0_y_pos,
                                                 self.icon0_x_pos + self.image_icon0.width,
                                                 self.icon0_y_pos + self.image_icon0.height))


        # A PIC0 must be used for the GUI: either existing
        if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC0.PNG')):
            tmp_pic0_bg = copy.copy(self.image_pic1)
        # or make with title text
        else:
            # else use background w/ title
            tmp_pic0_bg = copy.copy(self.image_pic1_w_title)
            # add ps3 system logo
            tmp_pic0_bg.paste(self.ps3_gametype_logo, (1180, 525), self.ps3_gametype_logo)
            # draw date and time beside ICON0
            self.draw_text_on_image_w_shadow(tmp_pic0_bg, "11/11/2006 00:00", 760, 522, 20, 1, 'white', 'black')

        # Image.paste(im1, (left, top, right, bottom), im1)
        tmp_pic0_bg.paste(self.image_pic0, (self.pic0_x_pos, self.pic0_y_pos), self.image_pic0)
        # Image.crop((left, top, right, bottom))
        tmp_image_pic0 = tmp_pic0_bg.crop((self.pic0_x_pos, self.pic0_y_pos,
                                               self.pic0_x_pos + self.image_pic0.width,
                                               self.pic0_y_pos + self.image_pic0.height))



        # resize: ->853, ->480
        self.photoimage_pic1 = PhotoImage(
            self.image_pic1.resize((int(1280 * self.scaling), int(720 * self.scaling)), Image.Resampling.LANCZOS))

        self.button_pic1 = Button(main,
                                  image=self.photoimage_pic1,
                                  highlightthickness=0,
                                  bd=0,
                                  command=lambda: self.image_replace_browser(main))

        CreateToolTip(self.button_pic1, self.PIC1_TOOLTIP_MSG)

        # ICON0 resizing
        icon0_x_scale = self.main_window_width / self.image_pic1.width * self.scaling
        icon0_y_scale = self.main_window_height / self.image_pic1.height * self.scaling

        self.icon0_new_dim = (
            int(icon0_x_scale * tmp_image_icon0.width), int(icon0_y_scale * tmp_image_icon0.height))

        self.image_icon0_resize = copy.copy(tmp_image_icon0)
        self.image_icon0_resize = self.image_icon0_resize.resize(
            (self.icon0_new_dim[0], self.icon0_new_dim[1]), Image.Resampling.LANCZOS)

        self.photoimage_icon0 = PhotoImage(self.image_icon0_resize)
        self.button_icon0 = Button(main,
                                   image=self.photoimage_icon0,
                                   highlightthickness=0,
                                   bd=0,
                                   command=lambda: self.image_replace_browser(main))
        CreateToolTip(self.button_icon0, self.ICON0_TOOLTIP_MSG)

        # PIC0 resizing
        pic0_x_scale = self.main_window_width / self.image_pic1.width * self.scaling
        pic0_y_scale = self.main_window_height / self.image_pic1.height * self.scaling

        self.pic0_new_dim = (
            int(pic0_x_scale * tmp_image_pic0.width), int(pic0_y_scale * tmp_image_pic0.height))

        self.image_pic0_resize = copy.copy(tmp_image_pic0)
        self.image_pic0_resize = self.image_pic0_resize.resize(
            (self.pic0_new_dim[0], self.pic0_new_dim[1]), Image.Resampling.LANCZOS)

        self.photo_image_pic0 = PhotoImage(self.image_pic0_resize)
        self.button_pic0 = Button(main,
                                   image=self.photo_image_pic0,
                                   highlightthickness=0,
                                   bd=0,
                                   command=lambda: self.image_replace_browser(main))
        CreateToolTip(self.button_pic0, self.PIC0_TOOLTIP_MSG)


        # finally placing ICON0, PIC0 and PIC1 onto the canvas
        self.button_pic1.place(x=self.pic1_button_x_pos * self.scaling, y=self.pic1_button_y_pos * self.scaling)
        self.button_pic0.place(x=int(self.pic0_button_x_pos * self.scaling), y=int(self.pic0_button_y_pos * self.scaling))
        self.button_icon0.place(x=int(self.icon0_button_x_pos * self.scaling), y=int(self.icon0_button_y_pos * self.scaling))

    def draw_text_on_image(self, image, text, text_x, text_y, text_size, text_color):
        font = ImageFont.truetype(os.path.join(self.fonts_path, 'SCE-PS3.ttf'), text_size)
        draw = ImageDraw.Draw(image)
        return draw.text((text_x, text_y), text, fill=text_color, font=font)

    def draw_text_on_image_w_font(self, image, text, text_x, text_y, text_size, text_color, font):
        if not os.path.isfile(font):
            print('ERROR: font does not exist')
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
            # print('DEBUG ' + '\'' + drive_choice + '\'' + ' already set')
            # if dev_usb### already set -> iterate port (0-3)
            if 'dev_usb00' in drive_choice:
                self.usb_port_number = self.usb_port_number + 1

                if self.usb_port_number > 3:
                    self.usb_port_number = 0
                # print('DEBUG usb_port_number: ' + str(self.usb_port_number))
                drive_choice = 'dev_usb00' + str(self.usb_port_number)

        # print('DEBUG drive_choice: ' + drive_choice)
        self.drive_system_path_array[0] = drive_choice

        current_iso_path = '/' + '/'.join([self.drive_system_path_array[0],
                                     self.drive_system_path_array[1],
                                     self.drive_system_path_array[2],
                                     self.entry_field_filename.get()]).replace('//', '/')

        self.update_iso_path_entry_field(current_iso_path)

    def on_system_button(self, drive_choice, system_choice):
        # print('DEBUG on_system_button')
        # if system_choice in self.entry_field_iso_path.get():
            # print('DEBUG ' + '\'' + system_choice + '\'' + ' already set')

        # print('DEBUG system_choice: ' + system_choice)
        self.drive_system_path_array[1] = system_choice

        current_iso_path = '/' + '/'.join([self.drive_system_path_array[0],
                                           self.drive_system_path_array[1],
                                           self.drive_system_path_array[2],
                                           self.entry_field_filename.get()]).replace('//', '/')

        self.update_iso_path_entry_field(current_iso_path)

        # Replace current drive
        if drive_choice not in current_iso_path:
            print('DEBUG drive_choice not in current_iso_path')
            print('DEBUG ' + '\'' + self.drive_system_path_array[0] + '\'' + ' changed -> ' + '\'' + drive_choice + '\'')
            current_iso_path = current_iso_path.replace(self.drive_system_path_array[0], drive_choice)
            self.update_iso_path_entry_field(current_iso_path)
            self.drive_system_path_array[0] = drive_choice

        # Replace current system
        if system_choice not in current_iso_path:
            print('DEBUG system_choice not in current_iso_path')
            print('DEBUG ' + '\'' + self.drive_system_path_array[1] + '\'' + ' changed -> ' + '\'' + system_choice + '\'')
            current_iso_path = current_iso_path.replace(self.drive_system_path_array[1], system_choice)
            self.update_iso_path_entry_field(current_iso_path)
            self.drive_system_path_array[1] = system_choice


    def on_save_button(self):
        if self.validate_fields():
            self.save_entry_to_game_list()

    # Dynamic update of the pkg path for showing fetched images
    def update_game_build_path(self):
        # ask gamelist to return selected path
        build_dir_pkg_path = None
        selected_path = self.game_list.get_selected_build_dir_path()
        if selected_path != '':
            AppPaths.game_work_dir = os.path.join(self.game_list.get_selected_build_dir_path(), 'work_dir')
            build_dir_pkg_path = os.path.join(AppPaths.game_work_dir, 'pkg')
        self.init_draw_images_on_canvas(self.main, pkg_build_path=build_dir_pkg_path)

    # Dynamic update of the 'entry_field_filename' into the 'entry_field_iso_path'
    def dynamic_filename_and_path(self, event):
        iso_path = ''
        drive = ''
        system = ''
        path = ''
        filename = self.entry_field_filename.get().replace('//', '/', )
        # TODO: this section could probably be optimized
        if self.drive_system_path_array[0] != None:
            drive = '/' + self.drive_system_path_array[0] + '/'
        if self.drive_system_path_array[1] != None:
            system = '/' + self.drive_system_path_array[1] + '/'
        if self.drive_system_path_array[2] != None:
            path = '/' + self.drive_system_path_array[2] + '/'

        if '' not in {drive, system, path, filename}:
            iso_path = drive + system + path + filename
            iso_path = iso_path.replace('//', '/', )

        self.entry_field_iso_path.xview_moveto(1)
        self.update_iso_path_entry_field(iso_path)

        if iso_path == '':
            # re-draw work_dir image on canvas
            self.__init_pkg_images__()
            self.init_draw_images_on_canvas(self.main)


    def update_iso_path_entry_field(self, iso_path):
            self.entry_field_iso_path.config(state='normal')
            self.entry_field_iso_path.delete(0, END)
            self.entry_field_iso_path.insert(0, iso_path.replace('//','/'))
            self.entry_field_iso_path.config(state='readonly')


    # Dynamic update of the game title on to the PIC1 image
    def dynamic_title_to_pic1(self, event):
        tmp_img = self.image_pic1
        # self, image, text, text_x, text_y, text_size, text_outline, text_color,
        self.draw_text_on_image_w_shadow(tmp_img, self.entry_field_title.get(), 760, 487, 32, 2, 'white', 'black')
        self.image_pic1_w_title = copy.copy(tmp_img)
        tmp_img = tmp_img.resize((int(1280 * self.scaling), int(720 * self.scaling)), Image.Resampling.LANCZOS)
        self.photo_image_pic1_xmb = PhotoImage(tmp_img)
        self.button_pic1.config(image=self.photo_image_pic1_xmb)
        self.init_draw_images_on_canvas(self.main)
        #TODO: this might be more optimized somewhere else
        self.update_game_build_path()


    def image_replace_browser(self, main):
        image = askopenfile(mode='rb', title='Browse an image', filetypes=[('PNG image', '.PNG')])
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
        import re
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

        if len(title_id) != self.title_id_maxlength:
            self.title_id_error_msg = 'Title id must be 9 characters long.'
            print(self.title_id_error_msg)
            self.entry_field_title_id.focus_set()
            self.entry_field_title_id.selection_range(0, END)
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
        tmp_name = filename
        # platform type GAMES has no file extension
        if self.entry_field_platform.get() == 'GAMES' and len(tmp_name) > 0:
            main_window.focus()
            return True
        # other platforms do have file extensions
        elif str(tmp_name).upper().endswith(GlobalVar.file_extensions) and len(tmp_name) > 4:
            main_window.focus()
            return True

        if len(tmp_name) < 1:
            self.filename_error_msg = 'DEBUG The file must have a name and any of the following extensions' + str(GlobalVar.file_extensions)
            print(self.filename_error_msg)
            self.entry_field_filename.focus_set()
            self.entry_field_filename.icursor(0)
            return False

        elif str(tmp_name).endswith(GlobalVar.file_extensions):
            self.filename_error_msg = 'DEBUG The image file must have a name'
            print(self.filename_error_msg)
            self.entry_field_filename.focus_set()
            self.entry_field_filename.icursor(0)
            return False

        else:
            self.filename_error_msg = 'DEBUG Filename \'' + filename + '\'' + ' must end on ' + str(GlobalVar.file_extensions)
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
            if not os.path.exists(AppPaths.game_work_dir):
                os.makedirs(os.path.join(AppPaths.game_work_dir, 'pkg'))

            # make sure we have the mandatory ICON0 in the build_dir
            if not os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'ICON0.PNG')):
                # find any donor platforms by using looking the entry field
                platform = ''
                if self.entry_field_platform == 'NTFS':
                    match = re.search('(?<=\[).*?(?=\])', str(self.entry_field_filename.get()))
                    if match != None:
                        donor_platform = filter(lambda x: match.group() in x[0], self.global_platform_paths)
                        if donor_platform:
                            platform = list(donor_platform)[0][1]

                default_img_path = os.path.join(AppPaths.resources, 'images', 'pkg', 'default')
                icon0 = Image.open(os.path.join(default_img_path, platform, 'ICON0.PNG')).convert("RGBA")
                icon0.save(os.path.join(AppPaths.game_work_dir, 'pkg', 'ICON0.PNG'))

            self.save_preview_image()
            self.save_pkg_info_to_json()

            # clean up the temp work dir
            __init_wcm_work_dir__(self)

            return True
        else:
            return False

    def save_entry_to_game_list(self):
        json_game_list = GameListData().get_game_list()
        current_work_dir = AppPaths.game_work_dir
        # save all changes to the current work_dir
        if self.save_work_dir():
            if not os.path.exists(self.pkg_dir):
                os.makedirs(self.pkg_dir)
            if not os.path.exists(AppPaths.game_work_dir):
                os.makedirs(current_work_dir)

        # if filepath already exist, remove game from json game list so we can update it
        platform_key = self.entry_field_platform.get() + '_games'
        if self.entry_field_platform.get() in {'GAMES', 'GAMEZ'}:
            path = '/'.join(self.entry_field_iso_path.get().split('/')[:-1])
            test_path1 = '/'.join(json_game_list[platform_key][0]['path'].split('/')[:-1])
            json_game_list[platform_key] = [x for x in json_game_list[platform_key] if '/'.join(x['path'].split('/')[:-1]) != path]
            print("test_path1: " + test_path1)
        else:
            path = self.entry_field_iso_path.get()
            test_path2 = json_game_list[platform_key][0]['path'] + json_game_list[platform_key][0]['filename']
            print("test_path2: " + test_path2)
            for test in json_game_list[platform_key]:
                if 'kingdom' in test['filename'].lower():
                    print(str(test['path'] +test['filename']))

            json_game_list[platform_key] = [x for x in json_game_list[platform_key] if str(x['path'] + x['filename']) != path]

        # update path to game work_dir
        AppPaths.game_work_dir = os.path.join(AppPaths().get_game_build_dir(self.entry_field_title_id.get(), self.entry_field_filename.get()), 'work_dir')
        if current_work_dir != AppPaths.game_work_dir:
            new_game_build_path = os.path.join(AppPaths.game_work_dir, '..')
            if not os.path.exists(new_game_build_path):
                os.mkdir(new_game_build_path)
            # copy old work_dir to new work_dir
            GlobalDef().copytree(os.path.join(current_work_dir, ''), AppPaths.game_work_dir)

            # remove old folder build folder
            if 'webman-classics-maker' in current_work_dir.lower():
                shutil.rmtree(os.path.join(current_work_dir, ''))

        # dup check title against list and update the title
        title = GameListData().duplicate_title_checker(self.entry_field_title.get())
        self.entry_field_title.delete(0, END)
        self.entry_field_title.insert(0, title)

        # add new data to the game list
        new_data_json = self.entry_fields_to_json(os.path.join(AppPaths.util_resources, 'game_structure.json.BAK'))
        json_game_list[platform_key].append(new_data_json)

        # update the json game list file
        with open(GameListData.GAME_LIST_DATA_PATH, 'w') as newFile:
            json_text = json.dumps(json_game_list, indent=4, separators=(",", ":"))
            newFile.write(json_text)

            # GameListData.game_list_data_json = GameListData().get_game_list()

        # change Appdata.work_dir
        AppPaths.game_work_dir = os.path.join(AppPaths().get_game_build_dir(self.entry_field_title_id.get(), self.entry_field_filename.get()), 'work_dir')


        # refresh the GUI list
        self.on_game_list_refresh()


    def on_build_button(self):
        __init_pkg_build_dir__()

        if self.save_work_dir():
            if not os.path.exists(self.pkg_dir):
                os.makedirs(self.pkg_dir)
            if not os.path.exists(AppPaths.game_work_dir):
                os.makedirs(AppPaths.game_work_dir)

            game_pkg_dir = os.path.join(AppPaths.game_work_dir, 'pkg')
            if os.path.isfile(os.path.join(game_pkg_dir, 'ICON0.PNG')):
                shutil.copyfile(os.path.join(game_pkg_dir, 'ICON0.PNG'), os.path.join(self.pkg_dir, 'ICON0.PNG'))
            else:
                # extract the platform name by using the path
                platform = ''
                if self.entry_field_platform == 'NTFS':
                    match = re.search('(?<=\[).*?(?=\])', str(self.entry_field_filename.get()))
                    if match != None:
                        # donor platform could be PS3 for game_name.NTFS[PS3]
                        donor_platform = filter(lambda x: match.group() in x[0], self.global_platform_paths)
                        if donor_platform:
                            platform = list(donor_platform)[0][1]

                # platform is used to determine which ICON0 should be used
                default_img_path = os.path.join(AppPaths.resources, 'images', 'pkg', 'default')
                if not os.path.isfile(os.path.join(default_img_path, platform, 'ICON0.PNG')):
                    platform = ''
                shutil.copyfile(os.path.join(default_img_path, platform, 'ICON0.PNG'), os.path.join(self.pkg_dir, 'ICON0.PNG'))

            if os.path.isfile(os.path.join(game_pkg_dir, 'PIC0.PNG')):
                shutil.copyfile(os.path.join(game_pkg_dir, 'PIC0.PNG'), os.path.join(self.pkg_dir, 'PIC0.PNG'))

            if os.path.isfile(os.path.join(game_pkg_dir, 'PIC1.PNG')):
                shutil.copyfile(os.path.join(game_pkg_dir, 'PIC1.PNG'), os.path.join(self.pkg_dir, 'PIC1.PNG'))

            # builds pkg and reads the pkg filename
            webman_pkg = Webman_PKG()

            pkg_name = webman_pkg.build()
            if pkg_name != None:
                # making sure default work_dir and pkg directories exists
                if not os.path.exists(game_pkg_dir):
                    os.makedirs(game_pkg_dir)

                    # saving the build content in the game build folder
                    GlobalDef().copytree(AppPaths.pkg, game_pkg_dir)

                if os.path.isdir(AppPaths.game_work_dir):
                    def popup():
                        install_path = self.drive_system_path_array[0]
                        remote_path = ''
                        if 'hdd0' in install_path:
                            pkg_remote_path = '/' + install_path + '/packages'
                        # usb
                        else:
                            pkg_remote_path = '/' + install_path + '/'

                        response = messagebox.askyesno('Build status: success', 'Build done!\nDo you want to remote-install the pkg?\n\nLocation: ' + pkg_remote_path + '/' + pkg_name)
                        # yes
                        if response:
                            pkg_local_path = os.path.join(AppPaths.game_work_dir, '../', pkg_name)

                            self.transfer_pkg(pkg_local_path, pkg_remote_path, pkg_name)
                            self.remote_install_pkg(pkg_remote_path, pkg_name)

                    # execute def popup()
                    popup()

                    # open builds folder in windows explorer
                    if 'win' in sys.platform:
                        # print('DEBUG opening folder: ' + os.path.join(AppPaths.game_work_dir, '..'))
                        try:
                            os.startfile(os.path.join(AppPaths.game_work_dir, '../'))
                        except:
                            print('ERROR: Could open the pkg build dir from Windows explorer')

            else:
                messagebox.showerror("Build status: fail", "Build failed!\nSee error log.")





    def on_ftp_fetch_button(self):
        # save the ps3-ip field to config file
        if self.entry_field_ftp_ip.get() != '':
            self.save_ftp_fields_on_fetch()
            ftp_game_list = FtpGameList(self.drive_dropdown.get(), self.platform_dropdown.get())
            ftp_game_list.execute()

            self.on_game_list_refresh()
        else:
            print('DEBUG cannot connect with empty ip.')


    def save_ftp_fields_on_fetch(self):
        # open make changes to existing settings file
        with open(self.ftp_settings_path, 'r') as settings_file:
            json_settings_data = json.load(settings_file)
            json_settings_data['ps3_lan_ip'] = str(self.entry_field_ftp_ip.get())
            json_settings_data['ftp_user'] = str(self.entry_field_ftp_user.get())
            json_settings_data['ftp_password'] = str(self.entry_field_ftp_pass.get())
            settings_file.close()
            
        # write changes to file
        with open(self.ftp_settings_path, 'w') as save_settings_file:
            new_json_data = json.dumps(json_settings_data, indent=4, separators=(",", ":"))
            save_settings_file.write(new_json_data)
            save_settings_file.close()

        # update FtpSettings
        FtpSettings.ps3_lan_ip = str(self.entry_field_ftp_ip.get())
        FtpSettings.ftp_user = str(self.entry_field_ftp_user.get())
        FtpSettings.ftp_password = str(self.entry_field_ftp_pass.get())



    def save_preview_image(self):
        # making a preview print of the game canvas

        # check for PIC1 as background for the preview
        if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC1.PNG')):
            pic1_img = Image.open(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC1.PNG')).convert("RGBA")
            preview_img = Image.open(os.path.join(AppPaths.resources, 'images', 'pkg', 'default', 'PIC1.PNG')).convert("RGBA")
            preview_img.paste(pic1_img, (0, 0), pic1_img)

        else:
            # if not, use a default background as PIC1
            preview_img = Image.open(os.path.join(AppPaths.resources, 'images', 'pkg', 'default', 'PIC1.PNG')).convert("RGBA")

        # check for PIC0 as background for the preview
        if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC0.PNG')):
            pic0_img = Image.open(os.path.join(AppPaths.game_work_dir, 'pkg', 'PIC0.PNG')).convert("RGBA")
            preview_img.paste(pic0_img, (self.pic0_x_pos, self.pic0_y_pos), pic0_img)
        else:
            # if no PIC0, use texts
            preview_img.paste(self.ps3_gametype_logo, (1180, 525), self.ps3_gametype_logo)
            self.draw_text_on_image_w_shadow(preview_img, "11/11/2006 00:00", 760, 522, 20, 1, 'white', 'black')
            self.draw_text_on_image_w_shadow(preview_img, str(self.entry_field_title.get()), 760, 487, 32, 2, 'white',
                                             'black')

        # check for ICON0 as background for the preview
        if os.path.isfile(os.path.join(AppPaths.game_work_dir, 'pkg', 'ICON0.PNG')):
            icon0_img = Image.open(os.path.join(AppPaths.game_work_dir, 'pkg', 'ICON0.PNG')).convert("RGBA")
            preview_img.paste(icon0_img, (self.icon0_x_pos, self.icon0_y_pos), icon0_img)

        preview_img.paste(self.image_xmb_icons, (0, 0), self.image_xmb_icons)
        preview_img.save(os.path.join(AppPaths.game_work_dir, '..', 'preview.png'))

    def on_game_list_refresh(self):
        if not self.platform_dropdown:
            self.list_filter_drive = 'ALL'
            self.list_filter_platform = 'ALL'
        else:
            self.list_filter_drive = self.drive_dropdown.get()
            self.list_filter_platform = self.platform_dropdown.get()
        self.create_dropdowns()

    def entry_fields_to_json(self, json_data_path):
        json_data = None
        if os.path.isfile(json_data_path):
            try:
                with open(json_data_path) as f:
                    json_data = json.load(f)
                    f.close()
            except ValueError as e:
                print("ERROR: File write error.")
                print(getattr(e, 'message', repr(e)))

        json_data['title'] = str(self.entry_field_title.get())

        if FtpSettings.use_w_title_id:
            json_data['title_id'] = 'W' + self.entry_field_title_id.get()[1:]
        else:
            json_data['title_id'] = self.entry_field_title_id.get()

        json_data['content_id'] = 'UP0001-' + str(json_data['title_id']) + '_00-0000000000000000'
        json_data['filename'] = str(self.entry_field_filename.get())
        json_data['platform'] = str(self.entry_field_platform.get())
        if str(self.entry_field_platform.get()) in {'GAMES', 'GAMEZ'}:
            json_data['path'] = str(self.entry_field_iso_path.get()).replace(str(self.entry_field_filename.get()), '').replace('//', '/')
        else:
            json_data['path'] = str(self.entry_field_iso_path.get()).replace(str(self.entry_field_filename.get()), '')

        return json_data

    def save_pkg_info_to_json(self):
            json_data = self.entry_fields_to_json(os.path.join(AppPaths.util_resources, 'pkg.json.BAK'))
            newFile = open(os.path.join(AppPaths.game_work_dir, 'pkg.json'), "w")
            json_text = json.dumps(json_data, indent=4, separators=(",", ":"))
            newFile.write(json_text)

    def transfer_pkg(self, pkg_local_path, pkg_remote_path, pkg_name):
        # setup connection to FTP
        try:
            ftp = FtpSettings().get_ftp()
            pkg_local_file = open(pkg_local_path, "rb")
            # go to path and transfer the pkg
            ftp.cwd(pkg_remote_path)
            ftp.storbinary('STOR ' + pkg_name, pkg_local_file)
            ftp.quit()

            print("DEBUG: Transfer succeeded")
            # messagebox.showinfo('Status: transfer complete', 'transfer of ' + pkg_name + ' to ' + remote_path + ' complete')
        except Exception as e:
            print ('ERROR: Transfer failed')
            print(getattr(e, 'message', repr(e)))

    def remote_install_pkg(self, pkg_remote_path, pkg_name):
        try:
            ps3_lan_ip = FtpSettings.ps3_lan_ip
            pkg_ps3_path = pkg_remote_path + '/' + pkg_name
            # webcommand = '/install_ps3' + urllib.parse.quote(pkg_ps3_path) # + '?restart.ps3'
            webcommand = '/install.ps3' + urllib.parse.quote(pkg_ps3_path) # + ';/refresh.ps3?xmb'
            webcommand_url = 'http://' + str(ps3_lan_ip) + webcommand
            print('DEBUG webcommand_url: ' + webcommand_url)
            response = urlopen(webcommand_url)
            status_code = response.getcode()
            print('DEBUG status_code: ' + str(status_code))
            if status_code == 200:
                messagebox.showinfo('Status: pkg installed', 'Install completed!')
            # 400 webman => faulty path => Error
            # 404 webman => faulty command => Not found
            # 200 OK
            print()
        except Exception as ez:
            print('ERROR: could not install pkg')
            print('DEBUG ERROR traceback: ' + str(traceback.print_exc()))
            print(getattr(ez, 'message', repr(ez)))

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

# scaling = 720.0 / 1080.0
# canvas_width = int(1920 * scaling)
# canvas_height = int(1080 * scaling)
# main_window_width = int(1920 * scaling)
# main_window_height = int(1080 * scaling)

Main()
main_window.mainloop()
