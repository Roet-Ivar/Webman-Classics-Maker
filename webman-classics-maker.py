#!/usr/bin/env python3
import copy
import json
import os
import shutil
import traceback
import urllib.parse
from urllib.request import urlopen
import sys
import re

# sudo apt-get install python3-tk
import tkinter as tk
from tkinter import *
from tkinter import messagebox
from tkinter.filedialog import askopenfile

from resources.tools.util_scripts.global_paths import (
    AppPaths,
    ImagePaths,
    GlobalVar,
    GlobalDef,
    FtpSettings,
    GameListData,
)
from resources.tools.util_scripts.build_all_scripts import Webman_PKG

from resources.tools.util_scripts.wcm_gui.drop_down import (
    DriveDropdown,
    PlatformDropdown,
)
from resources.tools.util_scripts.wcm_gui.ftp_game_data_fetcher import FtpGameList
from resources.tools.util_scripts.wcm_gui.game_listbox import Gamelist

if getattr(sys, "frozen", False):
    sys.path.append(
        os.path.join(
            os.path.dirname(sys.executable), "resources", "tools", "util_scripts"
        )
    )
    sys.path.append(
        os.path.join(
            os.path.dirname(sys.executable),
            "resources",
            "tools",
            "util_scripts",
            "wcm_gui",
        )
    )
else:
    # running webman_classics_maker.py from root
    app_full_path = os.path.realpath(__file__)
    application_path = os.path.dirname(app_full_path)
    sys.path.append(
        os.path.join(application_path, "resources", "tools", "util_scripts")
    )
    sys.path.append(
        os.path.join(application_path, "resources", "tools", "util_scripts", "wcm_gui")
    )

# pip install Pillow
from PIL import Image, ImageDraw, ImageFont
from PIL.ImageTk import PhotoImage


def __init_tmp_pkg_dir__():
    if os.path.isdir(AppPaths.tmp_work_dir):
        if "webman-classics-maker" in AppPaths.tmp_work_dir.lower():
            shutil.rmtree(AppPaths.tmp_work_dir)
    if not os.path.isdir(AppPaths.tmp_pkg_dir):
        os.makedirs(AppPaths.tmp_pkg_dir)

    GlobalDef().copytree(
        os.path.join(AppPaths.util_resources, "pkg_dir_bak"),
        os.path.join(AppPaths.tmp_pkg_dir),
    )


def __init_tmp_work_dir__():
    # clean and init wcm_work_dir in startup
    if os.path.isdir(AppPaths.tmp_work_dir):
        if "webman-classics-maker" in AppPaths.tmp_work_dir.lower():
            shutil.rmtree(AppPaths.tmp_work_dir)
    if not os.path.isdir(os.path.join(AppPaths.tmp_work_dir, "pkg")):
        os.makedirs(os.path.join(AppPaths.tmp_work_dir, "pkg"))


def get_build_dir_path(self, filename, title_id):
    self.build_dir_path = ""
    if filename not in {"", None}:
        build_base_path = AppPaths.builds
        tmp_filename = filename
        # removes the file extension from tmp_filename
        for file_ext in GlobalVar.file_extensions:
            if filename.upper().endswith(file_ext):
                tmp_filename = filename[0 : len(filename) - len(file_ext)]
                break
        game_folder_name = (
            tmp_filename.replace(" ", "_") + "_(" + title_id.replace("-", "") + ")"
        )

        self.build_dir_path = os.path.join(build_base_path, game_folder_name)
    return self.build_dir_path


def get_ftp_ip_from_config():
    return FtpSettings.ps3_lan_ip


def get_ftp_user_from_config():
    return FtpSettings.ftp_user


def get_ftp_pass_from_config():
    return FtpSettings.ftp_password


def get_default_image(filename):
    default_pkg_img_dir = os.path.join(ImagePaths.pkg, "default")
    return Image.open(os.path.join(default_pkg_img_dir, filename)).convert("RGBA")


def create_pic1_gui(self, active_pkg_dir):
    pic1_active_path = os.path.join(active_pkg_dir, "PIC1.PNG")
    if os.path.isfile(pic1_active_path):
        self.pic1_gui = Image.open(pic1_active_path).convert("RGBA")
        print(
            "use PIC1.PNG from {}".format(pic1_active_path)
        ) if self._verbose else None
    else:
        self.pic1_gui = Image.open(
            os.path.join(AppPaths.default_img_path, "PIC1.PNG")
        ).convert("RGBA")
        print(
            "use PIC1.PNG from {}".format(
                os.path.join(AppPaths.default_img_path, "PIC1.PNG")
            )
        ) if self._verbose else None

    # draw xmb icons and system logo onto the background
    self.pic1_gui.paste(self.image_xmb_icons, (0, 0), self.image_xmb_icons)
    self.pic1_gui.paste(self.ps3_gametype_logo, (1180, 525), self.ps3_gametype_logo)

    # draw game title text onto the background
    self.pic1_ref = copy.copy(self.pic1_gui)
    self.draw_text_on_image_w_shadow(
        self.pic1_gui,
        str(self.entry_field_title.get()),
        # 745, 457, 32, 2,
        760,
        487,
        32,
        2,
        "white",
        "black",
    )
    # self.draw_text_on_image_w_shadow(self.pic1_gui_w_title, self.entry_field_title.get(), 760, 487, 32, 2, 'white', 'black')

    # create photoimage to be used for the button
    self.pic1_photoimage = PhotoImage(
        self.pic1_gui.resize(
            (int(1280 * self.scaling), int(720 * self.scaling)),
            Image.Resampling.LANCZOS,
        )
    )

    # set the new background image
    self.pic1_button.config(image=self.pic1_photoimage)


def create_pic0_gui(self, active_pkg_dir):
    pic0_active_path = os.path.join(active_pkg_dir, "PIC0.PNG")

    if os.path.isfile(pic0_active_path):
        self.pic0_gui = Image.open(pic0_active_path).convert("RGBA")
        pic0_bg = copy.copy(self.pic1_gui)
        print(
            "use PIC0.PNG from {}".format(pic0_active_path)
        ) if self._verbose else None

    else:
        self.pic0_gui = Image.open(
            os.path.join(AppPaths.default_img_path, "PIC0.PNG")
        ).convert("RGBA")
        print(
            "use PIC0.PNG from {}".format(
                os.path.join(AppPaths.default_img_path, "PIC0.PNG")
            )
        ) if self._verbose else None
        # mask with PIC1 background
        # pic0_bg = copy.copy(self.pic1_gui_w_title)
        pic0_bg = copy.copy(self.pic1_gui)
        # add ps3 system logo
        pic0_bg.paste(self.ps3_gametype_logo, (1180, 525), self.ps3_gametype_logo)
        # draw date and time beside ICON0
        self.draw_text_on_image_w_shadow(
            pic0_bg, "11/11/2006 00:00", 760, 522, 20, 1, "white", "black"
        )

    self.pic0_x_pos = 750
    self.pic0_y_pos = 412

    # Image.paste(im1, (left, top, right, bottom), im1)
    pic0_bg.paste(self.pic0_gui, (self.pic0_x_pos, self.pic0_y_pos), self.pic0_gui)

    # Image.crop((left, top, right, bottom))
    tmp_image_pic0 = pic0_bg.crop(
        (
            self.pic0_x_pos,
            self.pic0_y_pos,
            self.pic0_x_pos + self.pic0_gui.width,
            self.pic0_y_pos + self.pic0_gui.height,
        )
    )

    # PIC0 resizing
    pic0_x_scale = self.main_window_width / self.pic1_gui.width * self.scaling
    pic0_y_scale = self.main_window_height / self.pic1_gui.height * self.scaling

    self.pic0_new_dim = (
        int(pic0_x_scale * tmp_image_pic0.width),
        int(pic0_y_scale * tmp_image_pic0.height),
    )

    self.image_pic0_resized = copy.copy(tmp_image_pic0).resize(
        (self.pic0_new_dim[0], self.pic0_new_dim[1]), Image.Resampling.LANCZOS
    )

    # create photoimage for the button
    self.pic0_photoimage = PhotoImage(self.image_pic0_resized)
    # set the new PIC0 button image
    self.pic0_button.config(image=self.pic0_photoimage)


def create_icon0_gui(self, active_pkg_dir):
    icon0_active_path = os.path.join(active_pkg_dir, "ICON0.PNG")
    platform = get_platform(self)

    if os.path.isfile(icon0_active_path):
        print(
            "use ICON0.PNG from {}".format(icon0_active_path)
        ) if self._verbose else None
        self.icon0_gui = Image.open(icon0_active_path).convert("RGBA")
    else:
        self.icon0_gui = Image.open(
            os.path.join(AppPaths.default_img_path, platform, "ICON0.PNG")
        ).convert("RGBA")
        print(
            "use ICON0.PNG from {}".format(
                os.path.join(AppPaths.default_img_path, platform, "ICON0.PNG")
            )
        )

    # image coordinates for the gui (w/o scaling)
    self.icon0_x_pos = 405
    self.icon0_y_pos = 416

    # blend ICON0 with PIC1 as background
    icon0_bg = copy.copy(self.pic1_gui)
    icon0_bg.paste(
        self.icon0_gui.convert("RGBA"),
        (self.icon0_x_pos, self.icon0_y_pos),
        self.icon0_gui.convert("RGBA"),
    )

    # Image.crop(left, top, right, bottom)
    icon0_bg = icon0_bg.crop(
        (
            self.icon0_x_pos,
            self.icon0_y_pos,
            self.icon0_x_pos + self.icon0_gui.width,
            self.icon0_y_pos + self.icon0_gui.height,
        )
    )
    # ICON0 resizing
    icon0_x_scale = self.main_window_width / self.pic1_gui.width * self.scaling
    icon0_y_scale = self.main_window_height / self.pic1_gui.height * self.scaling

    self.icon0_gui = copy.copy(icon0_bg)
    self.icon0_gui = self.icon0_gui.resize(
        (int(icon0_x_scale * icon0_bg.width), int(icon0_y_scale * icon0_bg.height)),
        Image.Resampling.LANCZOS,
    )

    # create photoimage for the button
    self.icon0_gui_photoimage = PhotoImage(self.icon0_gui)
    # set the new ICON0 button image
    self.icon0_button.config(image=self.icon0_gui_photoimage)


def get_platform(self):
    # extract the platform name by using the path
    try:
        platform = self.entry_field_platform.get() or ""
        if platform == "NTFS":
            match = re.search("(?<=[).*?(?=])", str(self.entry_field_filename.get()))
            if match is not None:
                donor_platform = list(
                    filter(lambda x: match.group() in x[0], GlobalVar.platform_paths)
                )
                if donor_platform:
                    platform = list(donor_platform)[0][1]
        return platform
    except AttributeError:
        return ""


class Main:
    def __init__(self):
        self.main = main_window
        self._verbose = True

        # window metrics
        self.scaling = 720.0 / 1080.0
        self.main_window_height = int(1080 * self.scaling)
        self.main_window_width = int(1920 * self.scaling)
        self.main_offset_x_pos = 1450
        self.main_offset_y_pos = 50

        # common paths
        self.WCM_BASE_PATH = AppPaths.wcm_gui
        self.tmp_work_dir = AppPaths.tmp_work_dir
        self.tmp_pkg_dir = AppPaths.tmp_pkg_dir
        self.builds_path = AppPaths.builds
        self.ftp_settings_path = os.path.join(AppPaths.settings, "ftp_settings.cfg")
        self.fonts_path = AppPaths.fonts
        self.game_pkg_dir = os.path.join(AppPaths.game_work_dir, "pkg")
        self.active_pkg_dir = self.game_pkg_dir

        # paddings
        self.text_box_x_padding = 20
        self.text_box_y_padding = 20
        self.text_box_spacing = 7 * self.text_box_x_padding

        # coordinates
        self.text_height = 15  # Font(font='Helvetica').metrics('linespace')
        self.device_text_y_pos = self.main_offset_y_pos + self.text_height
        self.type_text_y_pos = (
            self.text_box_y_padding + self.device_text_y_pos + self.text_height
        )
        self.title_id_text_y_pos = (
            self.text_box_y_padding + 7 + self.type_text_y_pos + self.text_height + 2
        )
        self.title_text_y_pos = (
            self.text_box_y_padding + self.title_id_text_y_pos + self.text_height
        )
        self.filename_text_y_pos = (
            self.text_box_y_padding + self.title_text_y_pos + self.text_height
        )
        self.iso_path_text_y_pos = (
            self.text_box_y_padding + self.filename_text_y_pos + self.text_height - 1
        )

        # init images and canvas for the gui
        self.drive_dropdown = None
        self.platform_dropdown = None
        self.main_canvas = None

        __init_tmp_pkg_dir__()
        self.__init_images_and_canvas__()
        self.__init_entry_fields__()
        self.__init_buttons__()
        self.__draw_background_on_canvas__()
        self.__draw_pkg_images_on_canvas__()

        self.__init_gamelist__()

    @property
    def verbose(self):
        return self._verbose

    @verbose.setter
    def verbose(self, value):
        self._verbose = value

    def __init_images_and_canvas__(self):
        # ui images
        self.image_xmb_icons = Image.open(os.path.join(ImagePaths.xmb, "XMB_icons.png"))
        self.ps3_gametype_logo = Image.open(
            os.path.join(ImagePaths.xmb, "ps3_type_logo.png")
        )

        self.hdd_button_image = PhotoImage(
            self.make_button_smallest("HDD", font="conthrax-sb.ttf", x=-1, y=-2)
        )
        self.usb_button_image = PhotoImage(
            self.make_button_smallest("USB", font="conthrax-sb.ttf", x=-1, y=-2)
        )
        self.psp_button_image = PhotoImage(
            self.make_button_smallest("PSP", font="conthrax-sb.ttf", x=-1, y=-2)
        )
        self.psx_button_image = PhotoImage(
            self.make_button_smallest("PSX", font="conthrax-sb.ttf", x=-1, y=-2)
        )
        self.ps2_button_image = PhotoImage(
            self.make_button_smallest("PS2", font="conthrax-sb.ttf", x=-1, y=-2)
        )
        self.ps3_button_image = PhotoImage(
            self.make_button_smallest("PS3", font="conthrax-sb.ttf", x=-1, y=-2)
        )
        self.build_button_image = PhotoImage(
            self.small_button_maker("Build", font="arial.ttf", x=3, y=0)
        )
        self.add_button_image = PhotoImage(
            self.small_button_maker("Add", font="arial.ttf", x=3, y=0)
        )
        self.save_button_image = PhotoImage(
            self.small_button_maker("Save", font="arial.ttf", x=3, y=0)
        )
        # self.quit_button_image = PhotoImage(self.make_smal_button('Quit', font='arial.ttf', x=3, y=0))
        # self.change_button_image = PhotoImage(self.make_smal_button('Change', font='arial.ttf', x=-3, y=0))
        self.fetch_button_image = PhotoImage(
            self.small_button_maker("Fetch", font="arial.ttf", x=3, y=0)
        )
        self.refresh_button_image = PhotoImage(
            self.small_button_maker("Refresh", font="arial.ttf", x=-1, y=0)
        )

        self.image_icon0 = get_default_image("ICON0.PNG")
        self.image_icon0_ref = copy.copy(self.image_icon0)

        self.pic0_gui = get_default_image("PIC0.PNG")
        self.gui_pic0_ref = copy.copy(self.pic0_gui)

        self.pic1_gui = get_default_image("PIC1.PNG")
        self.pic1_gui_ref = copy.copy(self.pic1_gui)
        self.pic1_gui_w_title = copy.copy(self.pic1_gui)
        self.pic1_gui_photoimage = None

        # ui background image
        self.background_images = []
        self.load_backgrounds()
        self.canvas_image_number = 0
        self.current_img = self.background_images[self.canvas_image_number]
        self.current_background = PhotoImage(self.current_img)

        self.main_canvas = Canvas(
            self.main,
            width=self.main_window_width,
            height=self.main_window_height,
            borderwidth=0,
            highlightthickness=0,
        )

        self.main_canvas.pack(fill=BOTH, expand=YES)

    def __init_entry_fields__(self):
        self.usb_port_number = 0
        self.drive_system_path_array = ["drive", "system", "path"]

        self.vcmd = self.main.register(self.dynamic_validate_title_id)
        self.vcmd2 = self.main.register(self.dynamic_validate_title_id)

        # entry fields
        self.entry_field_title_id = Entry(
            self.main, validate="key", validatecommand=(self.vcmd, "%P")
        )
        self.entry_field_title = Entry(self.main)
        self.entry_field_filename = Entry(self.main)
        self.entry_field_iso_path = Entry(self.main, state="readonly")
        # not visible in GUI
        self.entry_field_platform = Entry(self.main)

        ##########################################################################
        # Adding an on_change-listener on 'entry_field_title'
        self.generate_on_change(self.entry_field_title)
        self.entry_field_title.bind("<<Change>>", self.dynamic_title_to_pic1)
        ###########################################################################
        # Adding an on_change-listener on 'entry_field_filename'
        self.generate_on_change(self.entry_field_filename)
        ###########################################################################

        self.entry_field_ftp_ip = Entry(self.main)
        self.entry_field_ftp_ip.insert(0, get_ftp_ip_from_config())

        self.entry_field_ftp_user = Entry(self.main)
        self.entry_field_ftp_user.insert(0, get_ftp_user_from_config())

        self.entry_field_ftp_pass = Entry(self.main)
        self.entry_field_ftp_pass.insert(0, get_ftp_pass_from_config())

        # system choice buttons
        self.selection_drive_list = GlobalVar.drive_paths
        self.selection_system_list = GlobalVar.platform_paths
        self.drive_path = self.selection_drive_list[
            0
        ]  # drive should be toggled by buttons

        # Entry field placements
        entry_field_width = 200
        x1 = int((self.text_box_spacing + self.main_offset_x_pos) * self.scaling)
        x2 = int((self.main_offset_x_pos + 90) * self.scaling)
        x3 = int((self.main_offset_x_pos + 320) * self.scaling)

        self.entry_field_title_id.place(
            x=x1,
            y=int(self.title_id_text_y_pos * self.scaling),
            width=entry_field_width,
        )

        self.entry_field_title.place(
            x=x1, y=int(self.title_text_y_pos * self.scaling), width=entry_field_width
        )

        self.entry_field_filename.place(
            x=x1,
            y=int(self.filename_text_y_pos * self.scaling),
            width=entry_field_width,
        )

        self.entry_field_iso_path.place(
            x=x1,
            y=int(self.iso_path_text_y_pos * self.scaling),
            width=entry_field_width,
        )

        self.entry_field_ftp_ip.place(
            x=x2, y=int((self.main_offset_y_pos + 815) * self.scaling), width=90
        )

        self.entry_field_ftp_user.place(
            x=x3, y=int((self.main_offset_y_pos + 815) * self.scaling), width=60
        )

        self.entry_field_ftp_pass.place(
            x=x3, y=int((self.main_offset_y_pos + 850) * self.scaling), width=60
        )

    def __init_buttons__(self):
        print(self.selection_drive_list[0][0]) if self._verbose else None
        self.hdd_button = Button(
            self.main,
            image=self.hdd_button_image,
            borderwidth=1,
            command=lambda: self.on_drive_button(self.selection_drive_list[0][0]),
        )

        self.usb_button = Button(
            self.main,
            image=self.usb_button_image,
            borderwidth=1,
            command=lambda: self.on_drive_button(
                self.selection_drive_list[self.usb_port_number + 1][0]
            ),
        )

        self.psp_button = Button(
            self.main,
            image=self.psp_button_image,
            borderwidth=1,
            command=lambda: self.on_system_button(
                self.drive_system_path_array[0], self.selection_system_list[0][0]
            ),
        )

        self.psx_button = Button(
            self.main,
            image=self.psx_button_image,
            borderwidth=1,
            command=lambda: self.on_system_button(
                self.drive_system_path_array[0], self.selection_system_list[1][0]
            ),
        )

        self.ps2_button = Button(
            self.main,
            image=self.ps2_button_image,
            borderwidth=1,
            command=lambda: self.on_system_button(
                self.drive_system_path_array[0], self.selection_system_list[2][0]
            ),
        )

        self.ps3_button = Button(
            self.main,
            image=self.ps3_button_image,
            borderwidth=1,
            command=lambda: self.on_system_button(
                self.drive_system_path_array[0], self.selection_system_list[3][0]
            ),
        )

        self.build_button = Button(
            self.main,
            image=self.build_button_image,
            borderwidth=0,
            command=self.on_build_button,
            bg="#FBFCFB",
        )

        self.save_button = Button(
            self.main,
            image=self.save_button_image,
            borderwidth=0,
            command=self.on_save_button,
            bg="#FBFCFB",
        )

        self.fetch_button = Button(
            self.main,
            image=self.fetch_button_image,
            borderwidth=0,
            command=self.on_ftp_fetch_button,
            bg="#FBFCFB",
        )

        self.refresh_button = Button(
            self.main,
            image=self.refresh_button_image,
            borderwidth=0,
            command=self.__init_gamelist__,
            bg="#FBFCFB",
        )

        self.pic1_button = Button(
            self.main,
            highlightthickness=0,
            bd=0,
            command=lambda: self.image_replace_browser(),
        )

        self.pic0_button = Button(
            self.main,
            highlightthickness=0,
            bd=0,
            command=lambda: self.image_replace_browser(),
        )

        self.icon0_button = Button(
            self.main,
            highlightthickness=0,
            bd=0,
            command=lambda: self.image_replace_browser(),
        )

        # button tooltips
        CreateToolTip(self.usb_button, "Toggle USB port [0-3]")
        CreateToolTip(self.build_button, "Save & Build tmp_pkg_dir")
        CreateToolTip(self.save_button, "Save to builds folder")
        CreateToolTip(self.fetch_button, "Fetch gamelist and images over FTP")
        CreateToolTip(self.refresh_button, "Refresh gamelist from disk")
        CreateToolTip(self.pic1_button, "Replace PIC1")
        CreateToolTip(self.pic0_button, "Replace PIC0")
        CreateToolTip(self.icon0_button, "Replace ICON0")

        # Text button placements
        x1 = (self.text_box_spacing + self.main_offset_x_pos + 0 * 75) * self.scaling
        y1 = self.device_text_y_pos * self.scaling
        x2 = (self.text_box_spacing + self.main_offset_x_pos + 1 * 75) * self.scaling
        y2 = self.type_text_y_pos * self.scaling
        x3 = (self.text_box_spacing + self.main_offset_x_pos + 2 * 75) * self.scaling
        y3 = (self.iso_path_text_y_pos + 40) * self.scaling
        x4 = (self.text_box_spacing + self.main_offset_x_pos + 3 * 75) * self.scaling
        y4 = (self.main_offset_y_pos + 855) * self.scaling

        self.hdd_button.place(x=int(x1), y=int(y1))
        self.usb_button.place(x=int(x2), y=int(y1))

        self.psp_button.place(x=int(x1), y=int(y2))
        self.psx_button.place(x=int(x2), y=int(y2))
        self.ps2_button.place(x=int(x3), y=int(y2))
        self.ps3_button.place(x=int(x4), y=int(y2))

        self.build_button.place(x=int(x1), y=int(y3))
        self.save_button.place(x=int(x2 + 10), y=int(y3))

        self.fetch_button.place(x=int(self.main_offset_x_pos * self.scaling), y=int(y4))
        self.refresh_button.place(
            x=int(self.main_offset_x_pos * self.scaling + 60), y=int(y4)
        )

        # GUI buttons placements
        # image buttons coordinates (w/ scaling)
        pic1_button_x_pos = 75 * self.scaling
        pic1_button_y_pos = 175 * self.scaling
        pic0_button_x_pos = 573 * self.scaling
        pic0_button_y_pos = 450 * self.scaling
        icon0_button_x_pos = 344 * self.scaling
        icon0_button_y_pos = 454 * self.scaling

        self.pic1_button.place(x=pic1_button_x_pos, y=pic1_button_y_pos)

        self.pic0_button.place(x=int(pic0_button_x_pos), y=int(pic0_button_y_pos))

        self.icon0_button.place(x=int(icon0_button_x_pos), y=int(icon0_button_y_pos))

    def bind_filter_dropdowns(self):
        # ensure drive_dropdown into the listbox
        if self.drive_dropdown is None:
            self.drive_dropdown = DriveDropdown(self.main_canvas).get_dropdown()
        self.drive_dropdown.bind("<<ComboboxSelected>>", self.dropdown_filter_callback)

        # ensure platform_dropdown into the listbox
        if self.platform_dropdown is None:
            self.platform_dropdown = PlatformDropdown(self.main_canvas).get_dropdown()
        self.platform_dropdown.bind(
            "<<ComboboxSelected>>", self.dropdown_filter_callback
        )

    def dropdown_filter_callback(self, event):
        dropdown_name = str(event.widget).split(".")[-1]
        if dropdown_name == "drive_dropdown":
            self.list_filter_drive = event.widget.get()
            self.drive_dropdown.set(self.list_filter_drive)
        elif dropdown_name == "platform_dropdown":
            self.list_filter_platform = event.widget.get()
            self.platform_dropdown.set(self.list_filter_platform)

            # NTFS can only be used combined with HDD0
            if "NTFS" == self.list_filter_platform:
                self.list_filter_drive = "HDD0"
                self.drive_dropdown.set("HDD0")

        self.gamelist = Gamelist(
            self, self.list_filter_platform, self.list_filter_drive
        )

    def make_button_smallest(self, text, **args):
        font = None
        x = None
        y = None
        icon_bg_img = Image.new("RGB", (44, 15), color="black")
        for key, value in args.items():
            if "font" == key:
                font = value
            elif "x" == key:
                x = value
            elif "y" == key:
                y = value
            elif "width" == key:
                width = value
            elif "height" == key:
                height = value

        if not font:
            self.draw_text_on_image_w_font(
                icon_bg_img,
                text,
                7,
                3,
                12,
                "white",
                os.path.join(self.fonts_path, "arial.ttf"),
            )
        else:
            if x:
                x_val = x + 12 - len(text)
            else:
                x_val = 12 - len(text)

            self.draw_text_on_image_w_font(
                icon_bg_img,
                text,
                x_val,
                3 + y,
                10,
                "white",
                os.path.join(self.fonts_path, font),
            )

        return copy.copy(icon_bg_img)

    def small_button_maker(self, text, **args):
        font = None
        x = None
        y = None
        icon_bg_img = Image.new("RGB", (50, 20), color="black")
        for key, value in args.items():
            if "font" == key:
                font = value
            elif "x" == key:
                x = value
            elif "y" == key:
                y = value
            elif "width" == key:
                width = value
            elif "height" == key:
                height = value

        if not font:
            self.draw_text_on_image_w_font(
                icon_bg_img,
                text,
                7,
                3,
                12,
                "white",
                os.path.join(self.fonts_path, "arial.ttf"),
            )
        else:
            if x:
                x_val = x + 12 - len(text)
            else:
                x_val = 12 - len(text)

            self.draw_text_on_image_w_font(
                icon_bg_img,
                text,
                x_val,
                3 + y,
                12,
                "white",
                os.path.join(self.fonts_path, font),
            )

        return copy.copy(icon_bg_img)

    def medium_button_maker(self, text, *font_name):
        icon_bg_img = Image.new("RGB", (54, 20), color="black")
        if not font_name:
            self.draw_text_on_image_w_font(
                icon_bg_img,
                text,
                7,
                1,
                15,
                "white",
                os.path.join(self.fonts_path, "conthrax-sb.ttf"),
            )
        else:
            tmp_font = str(font_name[0])
            self.draw_text_on_image_w_font(
                icon_bg_img,
                text,
                7,
                1,
                15,
                "white",
                os.path.join(self.fonts_path, tmp_font),
            )
        return copy.copy(icon_bg_img)

    def __draw_background_on_canvas__(self):
        self.text_device = "Device"
        self.text_platform = "Type"

        self.text_title_id = "Title id"
        self.text_title = "Title"
        self.text_filename = "Filename"
        self.text_iso_path = "Path"

        self.text_ftp_game_list = "FTP Game list"
        self.text_ps3_ip_label = "PS3-ip"
        self.text_ps3_usr_label = "User"
        self.text_ps3_pass_label = "Pass"

        self.current_img = self.background_images[self.canvas_image_number]
        webman_logo = Image.open(
            os.path.join(ImagePaths.misc, "webman_text_icon_bw.png")
        ).resize((int(464 * 0.45), int(255 * 0.45)))

        self.draw_text_on_image_w_shadow(
            self.background_images[self.canvas_image_number],
            "webMAN",
            490,
            -10,
            110,
            6,
            "#0C55F4",
            "black",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_shadow(
            self.background_images[self.canvas_image_number],
            "Classics Maker",
            422,
            60,
            80,
            5,
            "white",
            "black",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.current_img.paste(webman_logo, (515, 22), webman_logo)

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_device.upper(),
            self.main_offset_x_pos,
            self.device_text_y_pos,
            25,
            "white",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_platform.upper(),
            self.main_offset_x_pos,
            self.type_text_y_pos,
            25,
            "white",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_title_id.upper(),
            self.main_offset_x_pos,
            self.title_id_text_y_pos,
            25,
            "white",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_title.upper(),
            self.main_offset_x_pos,
            self.title_text_y_pos,
            25,
            "white",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_filename.upper(),
            self.main_offset_x_pos,
            self.filename_text_y_pos,
            25,
            "white",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_iso_path.upper(),
            self.main_offset_x_pos,
            self.iso_path_text_y_pos,
            25,
            "white",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_ftp_game_list.upper(),
            self.main_offset_x_pos,
            self.iso_path_text_y_pos + 120,
            25,
            "white",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_ps3_ip_label.upper(),
            self.main_offset_x_pos + 0 * 50,
            self.main_offset_y_pos + 810,
            25,
            "#ffffff",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_ps3_usr_label.upper(),
            self.main_offset_x_pos + 5 * 50,
            self.main_offset_y_pos + 810,
            25,
            "#ffffff",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.draw_text_on_image_w_font(
            self.background_images[self.canvas_image_number],
            self.text_ps3_pass_label.upper(),
            self.main_offset_x_pos + 5 * 50,
            self.main_offset_y_pos + 845,
            25,
            "#ffffff",
            font=os.path.join(self.fonts_path, "LLPIXEL3.ttf"),
        )

        self.current_img = self.background_images[self.canvas_image_number]
        self.current_img = self.current_img.resize(
            (int(1920 * self.scaling), int(1080 * self.scaling)),
            Image.Resampling.LANCZOS,
        )

        self.tv_frame = Image.open(
            os.path.join(ImagePaths.misc, "tv_frame_1080_ps3_3.png")
        ).resize(
            (int(1990 * self.scaling), int(1327 * self.scaling)),
            Image.Resampling.LANCZOS,
        )
        self.current_img.paste(
            self.tv_frame,
            (int(45 * self.scaling), int(143 * self.scaling)),
            self.tv_frame,
        )

        self.background_image = self.main_canvas.create_image(
            0, 0, anchor=NW, image=self.current_background
        )
        self.current_background = PhotoImage(self.current_img)
        self.main_canvas.itemconfig(
            self.background_image, image=self.current_background
        )

    def load_backgrounds(self):
        base_path = os.path.join(ImagePaths.images, "backgrounds")
        dark = Image.open(os.path.join(base_path, "dark_transp.png"))
        for files in os.walk(base_path):
            for filenames in files:
                for file in filenames:
                    if any(ext in file for ext in ["png", "jpg"]):
                        # we dont want the dark transparency image to be a background
                        if "dark_transp.png" not in file:
                            tmp_img = Image.open(
                                os.path.join(base_path, base_path, file)
                            )
                            width, height = tmp_img.size
                            dark = dark.resize(((470 + 8), (height - 115 - 12)))
                            tmp_img.paste(dark, (width - (480 + 8), 12), dark)
                            self.background_images.append(tmp_img)

    def __draw_pkg_images_on_canvas__(self, **kwargs):
        img_to_be_changed = kwargs.get("img_to_be_changed", "").lower()
        self.active_pkg_dir = kwargs.get("game_pkg_dir", AppPaths.tmp_pkg_dir)
        print(
            "active_pkg_dir: {}".format(self.active_pkg_dir)
        ) if self._verbose else None

        if img_to_be_changed == "" or img_to_be_changed == "pic1":
            # redraw all images
            print("all - > all pkg images from active dir") if self._verbose else None

            create_pic1_gui(self, self.active_pkg_dir)
            create_pic0_gui(self, self.active_pkg_dir)
            create_icon0_gui(self, self.active_pkg_dir)

        elif img_to_be_changed == "pic0":
            # redraw all images
            print("pic0 -> pic0 and icon0 from active dir") if self._verbose else None
            create_pic0_gui(self, self.active_pkg_dir)

        elif img_to_be_changed == "icon0":
            # redraw all images
            print("icon0 -> icon0 from active dir") if self._verbose else None
            create_icon0_gui(self, self.active_pkg_dir)

    def draw_text_on_image(self, image, text, text_x, text_y, text_size, text_color):
        font = ImageFont.truetype(
            os.path.join(self.fonts_path, "SCE-PS3.ttf"), text_size
        )
        draw = ImageDraw.Draw(image)
        return draw.text((text_x, text_y), text, fill=text_color, font=font)

    def draw_text_on_image_w_font(
        self, image, text, text_x, text_y, text_size, text_color, font
    ):
        if not os.path.isfile(font):
            print("ERROR: font does not exist") if self._verbose else None
        font = ImageFont.truetype(font, text_size)
        draw = ImageDraw.Draw(image)
        return draw.text((text_x, text_y), text, fill=text_color, font=font)

    def draw_text_on_image_w_shadow(
        self,
        image,
        text,
        text_x,
        text_y,
        text_size,
        text_outline,
        text_color,
        shadow_color,
        **args
    ):
        if "font" in args:
            font = ImageFont.truetype(args["font"], text_size)
        else:
            font = ImageFont.truetype(
                os.path.join(self.fonts_path, "SCE-PS3.ttf"), text_size
            )

        if text_outline == None:
            text_outline = 2
        if text_color == None:
            text_outline = "white"
        if shadow_color == None:
            shadow_color = "black"

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

    def on_change_button(self):
        # next image
        self.canvas_image_number += 1

        # cycle back to first image
        if self.canvas_image_number == len(self.background_images):
            self.canvas_image_number = 0

        self.__draw_background_on_canvas__()

    def on_drive_button(self, drive_choice):
        print("DEBUG on_drive_button") if self._verbose else None
        # Check if same drive already set
        if drive_choice in self.entry_field_iso_path.get():
            # if dev_usb### already set -> iterate port (0-3)
            if "dev_usb00" in drive_choice:
                self.usb_port_number = self.usb_port_number + 1

                if self.usb_port_number > 3:
                    self.usb_port_number = 0
                drive_choice = "dev_usb00" + str(self.usb_port_number)

        print("DEBUG drive_choice: " + drive_choice) if self._verbose else None
        self.drive_system_path_array[0] = drive_choice

        current_iso_path = "/" + "/".join(
            [
                self.drive_system_path_array[0],
                self.drive_system_path_array[1],
                self.entry_field_filename.get(),
            ]
        ).replace("//", "/")

        self.update_iso_path_entry_field(current_iso_path)

    def on_system_button(self, drive_choice, system_choice):
        print("DEBUG system_choice: " + system_choice) if self._verbose else None
        self.drive_system_path_array[1] = system_choice

        current_iso_path = "/" + "/".join(
            [
                self.drive_system_path_array[0],
                self.drive_system_path_array[1],
                self.entry_field_filename.get(),
            ]
        ).replace("//", "/")

        self.update_iso_path_entry_field(current_iso_path)

        # Replace current drive
        if drive_choice not in current_iso_path:
            print(
                "DEBUG drive_choice not in current_iso_path"
            ) if self._verbose else None

            print(
                "DEBUG "
                + "'"
                + self.drive_system_path_array[0]
                + "'"
                + " changed -> "
                + "'"
                + drive_choice
                + "'"
            ) if self._verbose else None

            current_iso_path = current_iso_path.replace(
                self.drive_system_path_array[0], drive_choice
            )
            self.update_iso_path_entry_field(current_iso_path)
            self.drive_system_path_array[0] = drive_choice

        # Replace current system
        if system_choice not in current_iso_path:
            print(
                "DEBUG system_choice not in current_iso_path"
            ) if self._verbose else None

            print(
                "DEBUG "
                + "'"
                + self.drive_system_path_array[1]
                + "'"
                + " changed -> "
                + "'"
                + system_choice
                + "'"
            ) if self._verbose else None

            current_iso_path = current_iso_path.replace(
                self.drive_system_path_array[1], system_choice
            )
            self.update_iso_path_entry_field(current_iso_path)
            self.drive_system_path_array[1] = system_choice

    def on_save_button(self):
        if self.validate_fields():
            self.save_entry_to_game_list()

    # Dynamic update of the tmp_pkg_dir path for showing fetched images
    def update_game_build_path(self):
        # ask gamelist to return selected path
        selected_path = get_build_dir_path(
            self,
            str(self.entry_field_filename.get()),
            str(self.entry_field_title_id.get()),
        )
        if selected_path != "":
            AppPaths.game_work_dir = os.path.join(selected_path, "work_dir")
            self.game_pkg_dir = os.path.join(AppPaths.game_work_dir, "pkg")

        if self.game_pkg_dir == "pkg":
            self.game_pkg_dir = AppPaths.tmp_pkg_dir

        self.__draw_pkg_images_on_canvas__(game_pkg_dir=self.game_pkg_dir)

    def update_iso_path_entry_field(self, iso_path):
        self.entry_field_iso_path.config(state="normal")
        self.entry_field_iso_path.delete(0, END)
        self.entry_field_iso_path.insert(0, iso_path.replace("//", "/"))
        self.entry_field_iso_path.config(state="readonly")

    # Dynamic update of the game title on to the PIC1 image
    def dynamic_title_to_pic1(self, event):
        print("dynamic_title_to_pic1") if self._verbose else None
        self.pic1_gui_w_title = self.pic1_gui
        # self, image, text, text_x, text_y, text_size, text_outline, text_color,
        self.draw_text_on_image_w_shadow(
            self.pic1_gui_w_title,
            self.entry_field_title.get(),
            760,
            487,
            32,
            2,
            "white",
            "black",
        )
        tmp_img = self.pic1_gui_w_title.resize(
            (int(1280 * self.scaling), int(720 * self.scaling)),
            Image.Resampling.LANCZOS,
        )
        self.pic1_gui_photoimage = PhotoImage(tmp_img)
        self.pic1_button.config(image=self.pic1_gui_photoimage)
        self.update_game_build_path()

    def image_replace_browser(self):
        image = askopenfile(
            mode="rb", title="Browse an image", filetypes=[("PNG image", ".PNG")]
        )
        if image is not None:
            img_to_be_changed = None
            if self.active_pkg_dir in [None, ""]:
                self.active_pkg_dir = AppPaths.tmp_pkg_dir

            print("DEBUG image content:" + image.name) if self._verbose else None

            # Clear and replace image
            if "icon0" in image.name.lower():
                self.image_icon0 = Image.open(image)
                # self.image_icon0_ref = copy.copy(self.image_icon0)
                img_to_be_changed = "icon0"

                # save new image to both the active pkg dir folder
                if os.path.exists(self.active_pkg_dir):
                    self.image_icon0.save(
                        os.path.join(self.active_pkg_dir, "ICON0.PNG")
                    )

            elif "pic1" in image.name.lower():
                self.image_pic1 = Image.open(image)
                img_to_be_changed = "pic1"

                # save new image to both active pkg dir folder
                if os.path.exists(self.active_pkg_dir):
                    self.image_pic1.save(os.path.join(self.active_pkg_dir, "PIC1.PNG"))

            elif "pic0" in image.name.lower():
                self.pic0_gui = Image.open(image)
                img_to_be_changed = "pic0"

                # save new image to both active pkg dir folder
                if os.path.exists(self.active_pkg_dir):
                    self.pic0_gui.save(os.path.join(self.active_pkg_dir, "PIC0.PNG"))

            # # re-draw wcm_work_dir image on canvas
            self.__draw_pkg_images_on_canvas__(
                game_pkg_dir=self.active_pkg_dir, img_to_be_changed=img_to_be_changed
            )

    def generate_on_change(self, obj):
        obj.tk.eval(
            """
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
                """
        )
        obj.tk.eval(
            """
                rename {widget} _{widget}
                interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
            """.format(
                widget=str(obj)
            )
        )

    # Dynamic validation of title id
    def dynamic_validate_title_id(self, P):
        if len(P) > 0:
            P = P.upper()
            P = P.replace("-", "")
            P = re.sub(r"[^a-zA-Z0-9 -]", "", P)

            self.entry_field_title_id.delete(0, END)
            self.entry_field_title_id.insert(0, P[0:9])
            main_window.after_idle(
                lambda: self.entry_field_title_id.config(validate="key")
            )
            return True
        else:
            return False

    # Ensures title id is exactly 9 characters during save
    def validate_title_id_on_save(self):
        title_id = self.entry_field_title_id.get().upper()
        title_id = title_id.replace("_", "")
        title_id = title_id.replace("-", "")

        if len(title_id) != 9:
            self.title_id_error_msg = "Title id must be 9 characters long."
            print(self.title_id_error_msg) if self._verbose else None
            self.entry_field_title_id.focus_set()
            self.entry_field_title_id.selection_range(0, END)
            return False
        else:
            return True

    def validate_title_on_save(self):
        if len(self.entry_field_title.get()) > 0:
            return True
        else:
            self.title_error_msg = "Title cannot be empty."
            print(self.title_error_msg) if self._verbose else None
            self.entry_field_title.focus_set()
            self.entry_field_title.icursor(0)
            return False

    # Ensures title id is exactly 9 characters during save
    def validate_filename_on_save(self):
        filename = self.entry_field_filename.get()
        tmp_name = filename
        # platform 'GAMES' has no file extension
        if self.entry_field_platform.get() == "GAMES" and len(tmp_name) > 0:
            main_window.focus()
            return True
        # other platforms do have file extensions
        elif (
            str(tmp_name).upper().endswith(GlobalVar.file_extensions)
            and len(tmp_name) > 4
        ):
            main_window.focus()
            return True

        if len(tmp_name) < 1:
            filename_error_msg = (
                "DEBUG The file must have a name and any of the following extensions"
                + str(GlobalVar.file_extensions)
            )
            print(filename_error_msg) if self._verbose else None
            self.entry_field_filename.focus_set()
            self.entry_field_filename.icursor(0)
            return False

        elif str(tmp_name).endswith(GlobalVar.file_extensions):
            filename_error_msg = "DEBUG The image file must have a name"
            print(filename_error_msg) if self._verbose else None
            self.entry_field_filename.focus_set()
            self.entry_field_filename.icursor(0)
            return False

        else:
            filename_error_msg = (
                "DEBUG Filename '"
                + filename
                + "'"
                + " must end on "
                + str(GlobalVar.file_extensions)
            )
            print(filename_error_msg) if self._verbose else None
            self.entry_field_filename.focus_set()
            self.entry_field_filename.icursor(0)
            return False

    def validate_fields(self):
        if AppPaths.game_work_dir != "":
            print("DEBUG: wcm_work_dir: OK") if self._verbose else None
        else:
            return False

        if self.validate_title_id_on_save():
            print("DEBUG: Title_id: OK") if self._verbose else None
        else:
            return False
        if self.validate_title_on_save():
            print("DEBUG: Title: OK") if self._verbose else None
        else:
            return False
        if self.validate_filename_on_save():
            print("DEBUG: Title_id: OK") if self._verbose else None
        else:
            return False

        return True

    def save_work_dir(self):
        if self.validate_fields():
            if not os.path.exists(AppPaths.game_work_dir):
                print(
                    "create save_work_dir: {}".format(AppPaths.game_work_dir)
                ) if self._verbose else None

                if AppPaths.game_work_dir == "":
                    # we need to build the path first
                    selected_path = self.gamelist.get_selected_build_dir_path(
                        str(self.entry_field_filename.get()),
                        str(self.entry_field_title_id.get()),
                    )
                    AppPaths.game_work_dir = os.path.join(selected_path, "work_dir")
                    self.game_pkg_dir = os.path.join(AppPaths.game_work_dir, "pkg")

                print(
                    "Creating game_work_dir: "
                    + str(os.path.join(AppPaths.game_work_dir, "pkg"))
                ) if self._verbose else None
                os.makedirs(os.path.join(AppPaths.game_work_dir, "pkg"))

                GlobalDef().copytree(self.tmp_work_dir, AppPaths.game_work_dir)

            self.save_preview_image()
            self.save_pkg_info_to_json()

            # clean up the temp work dir
            __init_tmp_work_dir__()

            return True
        else:
            return False

    def save_entry_to_game_list(self):
        json_game_list = GameListData().get_game_list_from_disk()
        current_work_dir = AppPaths.game_work_dir
        # save all changes to the current wcm_work_dir
        if self.save_work_dir():
            if not os.path.exists(self.tmp_pkg_dir):
                os.makedirs(self.tmp_pkg_dir)
            if not os.path.exists(AppPaths.game_work_dir):
                os.makedirs(current_work_dir)

        # if filepath already exist, remove game from json game list so we can update it
        platform = self.entry_field_platform.get() + "_games"
        if self.entry_field_platform.get() in {"GAMES", "GAMEZ"}:
            path = "/".join(self.entry_field_iso_path.get().split("/")[:-1])
            test_path1 = "/".join(json_game_list[platform][0]["path"].split("/")[:-1])
            json_game_list[platform] = [
                x
                for x in json_game_list[platform]
                if "/".join(x["path"].split("/")[:-1]) != path
            ]
            print("test_path1: " + test_path1) if self._verbose else None
        else:
            path = self.entry_field_iso_path.get()
            test_path2 = (
                json_game_list[platform][0]["path"]
                + json_game_list[platform][0]["filename"]
            )
            print("test_path2: " + test_path2) if self._verbose else None
            for test in json_game_list[platform]:
                if "kingdom" in test["filename"].lower():
                    print(
                        str(test["path"] + test["filename"])
                    ) if self._verbose else None

            json_game_list[platform] = [
                x
                for x in json_game_list[platform]
                if str(x["path"] + x["filename"]) != path
            ]

        # update path to game wcm_work_dir
        AppPaths.game_work_dir = os.path.join(
            AppPaths().get_game_build_dir(
                self.entry_field_title_id.get(), self.entry_field_filename.get()
            ),
            "wcm_work_dir",
        )
        if current_work_dir != AppPaths.game_work_dir:
            new_game_build_path = os.path.join(AppPaths.game_work_dir, "..")
            if not os.path.exists(new_game_build_path):
                os.mkdir(new_game_build_path)
            # copy old wcm_work_dir to new wcm_work_dir
            GlobalDef().copytree(
                os.path.join(current_work_dir, ""), AppPaths.game_work_dir
            )

            # remove old folder build folder
            if "webman-classics-maker" in current_work_dir.lower():
                shutil.rmtree(os.path.join(current_work_dir, ""))

        # dup check title against list and update the title
        title = GameListData().duplicate_title_fixer(
            self.entry_field_title.get(),
            self.entry_field_iso_path.get(),
            self.entry_field_filename.get(),
        )
        self.entry_field_title.delete(0, END)
        self.entry_field_title.insert(0, title)

        # add new data to the game list
        new_data_json = self.entry_fields_to_json(
            os.path.join(AppPaths.util_resources, "game_structure.json.BAK")
        )
        json_game_list[platform].append(new_data_json)

        # update the json game list file
        with open(GameListData.GAME_LIST_DATA_PATH, "w") as newFile:
            json_text = json.dumps(json_game_list, indent=4, separators=(",", ":"))
            newFile.write(json_text)

            # GameListData.game_list_data_json = GameListData().get_game_list()

        # change Appdata.wcm_work_dir
        AppPaths.game_work_dir = os.path.join(
            AppPaths().get_game_build_dir(
                self.entry_field_title_id.get(), self.entry_field_filename.get()
            ),
            "wcm_work_dir",
        )

    def on_build_button(self):
        self.update_game_build_path()

        if self.save_work_dir():
            if not os.path.exists(self.tmp_pkg_dir):
                os.makedirs(self.tmp_pkg_dir)
            if not os.path.exists(AppPaths.game_work_dir):
                os.makedirs(AppPaths.game_work_dir)

            __init_tmp_pkg_dir__()

            self.game_pkg_dir = os.path.join(AppPaths.game_work_dir, "pkg")
            if os.path.isfile(os.path.join(self.game_pkg_dir, "ICON0.PNG")):
                shutil.copyfile(
                    os.path.join(self.game_pkg_dir, "ICON0.PNG"),
                    os.path.join(self.tmp_pkg_dir, "ICON0.PNG"),
                )
            else:
                # extract the platform name by using the path
                platform = ""
                if self.entry_field_platform == "NTFS":
                    match = re.search(
                        "(?<=\[).*?(?=\])", str(self.entry_field_filename.get())
                    )
                    if match != None:
                        # donor platform could be PS3 for game_name.NTFS[PS3]
                        donor_platform = list(
                            filter(
                                lambda x: match.group() in x[0],
                                GlobalVar.platform_paths,
                            )
                        )
                        if donor_platform:
                            platform = list(donor_platform)[0][1]

                # platform is used to determine which ICON0 should be used
                default_img_path = os.path.join(
                    AppPaths.resources, "images", "pkg", "default"
                )
                if not os.path.isfile(
                    os.path.join(default_img_path, platform, "ICON0.PNG")
                ):
                    platform = ""
                shutil.copyfile(
                    os.path.join(default_img_path, platform, "ICON0.PNG"),
                    os.path.join(self.tmp_pkg_dir, "ICON0.PNG"),
                )

            if os.path.isfile(os.path.join(self.game_pkg_dir, "PIC0.PNG")):
                shutil.copyfile(
                    os.path.join(self.game_pkg_dir, "PIC0.PNG"),
                    os.path.join(self.tmp_pkg_dir, "PIC0.PNG"),
                )

            if os.path.isfile(os.path.join(self.game_pkg_dir, "PIC1.PNG")):
                shutil.copyfile(
                    os.path.join(self.game_pkg_dir, "PIC1.PNG"),
                    os.path.join(self.tmp_pkg_dir, "PIC1.PNG"),
                )

            # builds tmp_pkg_dir and reads the tmp_pkg_dir filename
            pkg_name = Webman_PKG().build()

            if pkg_name != None:
                # making sure default wcm_work_dir and tmp_pkg_dir directories exists
                if not os.path.exists(self.game_pkg_dir):
                    os.makedirs(self.game_pkg_dir)

                    # saving the build content in the game build folder
                    GlobalDef().copytree(AppPaths.tmp_pkg_dir, self.game_pkg_dir)

                if os.path.isdir(AppPaths.game_work_dir):
                    install_path = self.drive_system_path_array[0]
                    if "hdd0" in install_path:
                        pkg_remote_path = "/" + install_path + "/packages"
                    # any usb
                    else:
                        pkg_remote_path = "/" + install_path + "/"

                    response = messagebox.askyesno(
                        "Build status: success",
                        "Build done!\nDo you want to remote-install the tmp_pkg_dir?\n\nLocation: "
                        + pkg_remote_path
                        + "/"
                        + pkg_name,
                    )
                    # yes
                    if response:
                        pkg_local_path = os.path.join(
                            AppPaths.game_work_dir, "../", pkg_name
                        )

                        self.transfer_pkg(pkg_local_path, pkg_remote_path, pkg_name)
                        self.remote_install_pkg(pkg_remote_path, pkg_name)

                    # open builds folder in windows explorer
                    if "win" in sys.platform:
                        try:
                            os.startfile(os.path.join(AppPaths.game_work_dir, "../"))
                        except:
                            print(
                                "ERROR: Could open the tmp_pkg_dir build dir from Windows explorer"
                            ) if self._verbose else None

            else:
                messagebox.showerror(
                    "Build status: fail", "Build failed!\nSee error log."
                )

    def on_ftp_fetch_button(self):
        response = messagebox.askyesno(
            "FTP fetch", "This will overwrite your current gamelist, continue?"
        )
        # yes
        if response:
            # save the ps3-ip field to config file
            if self.entry_field_ftp_ip.get() != "":
                self.save_ftp_fields_on_fetch()
                ftp_game_list = FtpGameList(
                    self.drive_dropdown.get(), self.platform_dropdown.get()
                )
                ftp_game_list.execute(
                    self.drive_dropdown.get(), self.platform_dropdown.get()
                )

                self.__init_gamelist__()
            else:
                print("DEBUG cannot connect with empty ip.") if self._verbose else None

    def save_ftp_fields_on_fetch(self):
        # open make changes to existing settings file
        with open(self.ftp_settings_path, "r") as settings_file:
            json_settings_data = json.load(settings_file)
            json_settings_data["ps3_lan_ip"] = str(self.entry_field_ftp_ip.get())
            json_settings_data["ftp_user"] = str(self.entry_field_ftp_user.get())
            json_settings_data["ftp_password"] = str(self.entry_field_ftp_pass.get())
            settings_file.close()

        # write changes to file
        with open(self.ftp_settings_path, "w") as save_settings_file:
            new_json_data = json.dumps(
                json_settings_data, indent=4, separators=(",", ":")
            )
            save_settings_file.write(new_json_data)
            save_settings_file.close()

        # update FtpSettings
        FtpSettings.ps3_lan_ip = str(self.entry_field_ftp_ip.get())
        FtpSettings.ftp_user = str(self.entry_field_ftp_user.get())
        FtpSettings.ftp_password = str(self.entry_field_ftp_pass.get())

    def save_preview_image(self):
        # making a preview print of the game canvas
        print(
            "saving preview at {}".format(self.active_pkg_dir)
        ) if self._verbose else None
        # check for PIC1 as background for the preview
        if os.path.isfile(os.path.join(self.active_pkg_dir, "PIC1.PNG")):
            pic1_img = Image.open(
                os.path.join(self.active_pkg_dir, "PIC1.PNG")
            ).convert("RGBA")
            preview_img = Image.open(
                os.path.join(AppPaths.resources, "images", "pkg", "default", "PIC1.PNG")
            ).convert("RGBA")
            preview_img.paste(pic1_img, (0, 0), pic1_img)

        else:
            # if not, use a default background as PIC1
            preview_img = Image.open(
                os.path.join(AppPaths.resources, "images", "pkg", "default", "PIC1.PNG")
            ).convert("RGBA")

        # check for PIC0 as background for the preview
        if os.path.isfile(os.path.join(AppPaths.game_work_dir, "pkg", "PIC0.PNG")):
            pic0_img = Image.open(
                os.path.join(AppPaths.game_work_dir, "pkg", "PIC0.PNG")
            ).convert("RGBA")
            preview_img.paste(pic0_img, (self.pic0_x_pos, self.pic0_y_pos), pic0_img)
        else:
            # if no PIC0, use texts
            preview_img.paste(
                self.ps3_gametype_logo, (1180, 525), self.ps3_gametype_logo
            )
            self.draw_text_on_image_w_shadow(
                preview_img, "11/11/2006 00:00", 760, 522, 20, 1, "white", "black"
            )
            self.draw_text_on_image_w_shadow(
                preview_img,
                str(self.entry_field_title.get()),
                760,
                487,
                32,
                2,
                "white",
                "black",
            )

        # check for ICON0 as background for the preview
        if os.path.isfile(os.path.join(AppPaths.game_work_dir, "pkg", "ICON0.PNG")):
            icon0_img = Image.open(
                os.path.join(AppPaths.game_work_dir, "pkg", "ICON0.PNG")
            ).convert("RGBA")
            preview_img.paste(
                icon0_img, (self.icon0_x_pos, self.icon0_y_pos), icon0_img
            )

        preview_img.paste(self.image_xmb_icons, (0, 0), self.image_xmb_icons)
        preview_img.save(os.path.join(AppPaths.game_work_dir, "..", "preview.png"))

    def __init_gamelist__(self):
        if not self.platform_dropdown:
            self.list_filter_drive = "all"
            self.list_filter_platform = "all"
        else:
            self.list_filter_drive = self.drive_dropdown.get()
            self.list_filter_platform = self.platform_dropdown.get()

        self.gamelist = Gamelist(self)
        self.bind_filter_dropdowns()

    def entry_fields_to_json(self, json_data_path):
        json_data = None
        if os.path.isfile(json_data_path):
            try:
                with open(json_data_path) as f:
                    json_data = json.load(f)
                    f.close()
            except ValueError as e:
                print("ERROR: File write error.") if self._verbose else None
                print(getattr(e, "message", repr(e))) if self._verbose else None

        json_data["title"] = str(self.entry_field_title.get())

        if FtpSettings.use_w_title_id:
            json_data["title_id"] = "W" + self.entry_field_title_id.get()[1:]
        else:
            json_data["title_id"] = self.entry_field_title_id.get()

        json_data["content_id"] = (
            "UP0001-" + str(json_data["title_id"]) + "_00-0000000000000000"
        )
        json_data["filename"] = str(self.entry_field_filename.get())
        json_data["platform"] = str(self.entry_field_platform.get())
        if str(self.entry_field_platform.get()) in {"GAMES", "GAMEZ"}:
            json_data["path"] = (
                str(self.entry_field_iso_path.get())
                .replace(str(self.entry_field_filename.get()), "")
                .replace("//", "/")
            )
        else:
            json_data["path"] = str(self.entry_field_iso_path.get()).replace(
                str(self.entry_field_filename.get()), ""
            )

        return json_data

    def save_pkg_info_to_json(self):
        json_data = self.entry_fields_to_json(
            os.path.join(AppPaths.util_resources, "pkg.json.BAK")
        )
        newFile = open(os.path.join(AppPaths.game_work_dir, "pkg.json"), "w")
        json_text = json.dumps(json_data, indent=4, separators=(",", ":"))
        newFile.write(json_text)

    def transfer_pkg(self, pkg_local_path, pkg_remote_path, pkg_name):
        # setup connection to FTP
        try:
            ftp = FtpSettings().get_ftp()
            pkg_local_file = open(pkg_local_path, "rb")
            # go to path and transfer the tmp_pkg_dir
            ftp.cwd(pkg_remote_path)
            ftp.storbinary("STOR " + pkg_name, pkg_local_file)
            ftp.quit()

            print("DEBUG: Transfer succeeded") if self._verbose else None
            # messagebox.showinfo('Status: transfer complete', 'transfer of ' + pkg_name + ' to ' + remote_path + ' complete')
        except Exception as e:
            print("ERROR: Transfer failed") if self._verbose else None
            print(getattr(e, "message", repr(e))) if self._verbose else None

    def remote_install_pkg(self, pkg_remote_path, pkg_name):
        try:
            ps3_lan_ip = FtpSettings.ps3_lan_ip
            pkg_ps3_path = pkg_remote_path + "/" + pkg_name
            # webcommand = '/install_ps3' + urllib.parse.quote(pkg_ps3_path) # + '?restart.ps3'
            webcommand = "/install.ps3" + urllib.parse.quote(
                pkg_ps3_path
            )  # + ';/refresh.ps3?xmb'
            webcommand_url = "http://" + str(ps3_lan_ip) + webcommand
            print("DEBUG webcommand_url: " + webcommand_url) if self._verbose else None
            response = urlopen(webcommand_url)
            status_code = response.getcode()
            print("DEBUG status_code: " + str(status_code)) if self._verbose else None
            if status_code == 200:
                messagebox.showinfo(
                    "Status: tmp_pkg_dir installed", "Install completed!"
                )
            # status 400: webman => faulty path => Error
            # status 404: webman => faulty command => Not found
            # status 200: OK
        except Exception as ez:
            print("ERROR: could not install tmp_pkg_dir") if self._verbose else None
            print(
                "DEBUG ERROR traceback: " + str(traceback.print_exc())
            ) if self._verbose else None
            print(getattr(ez, "message", repr(ez))) if self._verbose else None


class CreateToolTip(object):
    """
    create a tooltip for a given widget
    """

    def __init__(self, widget, text="widget info"):
        self.waittime = 350  # miliseconds
        self.wraplength = 180  # pixels
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
        label = tk.Label(
            self.tw,
            text=self.text,
            justify="left",
            background="#ffffff",
            relief="solid",
            borderwidth=1,
            wraplength=self.wraplength,
        )
        label.pack(ipadx=1)

    def hidetip(self):
        tw = self.tw
        self.tw = None
        if tw:
            tw.destroy()


# setup properties
main_window = Tk()
main_window.geometry("+%d+%d" % (0, 0))
main_window.title("Webman Classics Maker")

# icon upper left corner
if "linux" in sys.platform:
    main_window.iconbitmap("@" + os.path.join(ImagePaths.misc, "webman_icon.xbm"))
elif "win" in sys.platform:
    main_window.iconbitmap(os.path.join(ImagePaths.misc, "webman.ico"))

Main()
main_window.mainloop()
