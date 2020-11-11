from Tkinter import Frame, Scrollbar, Listbox, LEFT, RIGHT, Y, END, Label, Menu
import json, os, sys, shutil
from shutil import copyfile
sys.path.append('..')
from global_paths import App as AppPaths
from global_paths import GlobalVar
from global_paths import GameListData

class Gamelist():
    def __init__(self, drive, platform):
        GameListData.game_list_data_json = GameListData().get_game_list()
        self.json_game_list_data = GameListData.game_list_data_json

        if drive == 'USB(*)':
            self.drive_to_show = '/dev_' + drive.lower().replace('(*)', '')
        else:
            self.drive_to_show = '/dev_' + drive.lower() + '/'

        self.platform_to_show = platform + '_games'
        self.WCM_BASE_PATH  = AppPaths.wcm_gui
        self.last_selection = (None, 0)
        self.list_of_items = []

        self.selected_title_id   = None
        self.selected_title      = None
        self.selected_path       = None
        self.selected_filename   = None
        self.drive_system_path_array = None

        self.is_cleared = False


    def create_main_frame(self, entry_field_title_id, entry_field_title, entry_field_filename, entry_field_iso_path, entry_field_platform, drive_system_array):
        self.entry_field_title_id       = entry_field_title_id
        self.entry_field_title          = entry_field_title
        self.entry_field_filename       = entry_field_filename
        self.entry_field_iso_path       = entry_field_iso_path
        self.entry_field_platform       = entry_field_platform
        self.drive_system_path_array    = drive_system_array

        self.corrected_index = []
        self.main_frame = Frame()

        self.popup_menu = Menu(self.main_frame, tearoff=0)

        self.popup_menu.add_command(label="Delete",
                                    command=self.delete_selected)
        self.popup_menu.add_command(label="Rename",
                                    command=self.rename_selected)
        # self.popup_menu.add_command(label="Refetch",
        #                             command=self.refetch)
        # self.popup_menu.add_command(label="Select All",
        #                             command=self.select_all)




        s = Scrollbar(self.main_frame)
        self._listbox = Listbox(self.main_frame, width=465)
        self._listbox.bind('<Enter>', self._bound_to_mousewheel)
        self._listbox.bind('<Leave>', self._unbound_to_mousewheel)
        self._listbox.bind("<Button-3>", self.popup) # Button-2 on Aqua

        s.pack(side=RIGHT, fill=Y)
        self._listbox.pack(side=LEFT, fill=Y)

        s['command'] = self._listbox.yview
        self._listbox['yscrollcommand'] = s.set



        # default filters
        if 'ALL_games' == self.platform_to_show:
            # iterate all platforms
            for platform in self.json_game_list_data:
                for list_game in self.json_game_list_data[platform]:
                    # titles in the list has been designed to be unique
                    if '/dev_all/' == self.drive_to_show or self.drive_to_show in list_game['path']:
                        self.add_item(list_game['title'])

        else:
            for list_game in self.json_game_list_data[self.platform_to_show]:
                if '/dev_all/' == self.drive_to_show or self.drive_to_show in list_game['path']:
                    self.add_item(list_game['title'])

        for x in range(19 - self._listbox.size()):
            self.add_item('')


        # adding shade to every other row of the list
        for x in range(0, self._listbox.size()):
            if x % 2 == 0:
                self._listbox.itemconfig(x, {'fg': 'white'}, background='#001738')
            else:
                self._listbox.itemconfig(x, {'fg': 'white'}, background='#001F4C')

        self.label = Label(self.main_frame)
        self.selection_poller()

        return self.main_frame

    def selection_poller(self):
        self.label.after(200, self.selection_poller)
        self.new_selection = self._listbox.curselection()
        # cursor har been initiated
        if self._listbox.curselection() is not ():
            if self.new_selection[0] is not self.last_selection[0] or self.is_cleared:
                self.entry_fields_update(self.new_selection)
                self.is_cleared = False
                self.last_selection = self.new_selection


    def entry_fields_update(self, new_selection):
        for platform in self.json_game_list_data:

            for list_game in self.json_game_list_data[platform]:
                self.selected_title = self._listbox.get(new_selection[0])
                tmp_title = list_game['title']

                match = self.selected_title == str(tmp_title)
                if match:
                    self.selected_title_id   = str(list_game['title_id']).replace('-', '')
                    self.selected_title      = str(list_game['title'])
                    self.selected_path       = str(list_game['path'])
                    self.selected_filename   = str(list_game['filename'])
                    self.selected_platform   = str(list_game['platform'])

                    # parse drive and system from json data
                    path_array = filter(None, self.selected_path.split('/'))
                    self.drive_system_path_array[0] = path_array[0]
                    self.drive_system_path_array[1] = path_array[1]
                    self.drive_system_path_array[2] = '/'.join(path_array[2:len(path_array)]).replace('//', '')


                    self.entry_field_title_id.delete(0, len(self.entry_field_title_id.get())-1)
                    self.entry_field_title_id.delete(0, END)
                    self.entry_field_title_id.insert(0, self.selected_title_id)

                    self.entry_field_title.delete(0, END)
                    self.entry_field_title.insert(0, self.selected_title)

                    self.entry_field_filename.delete(0, END)
                    self.entry_field_filename.insert(0, self.selected_filename)

                    self.entry_field_platform.delete(0, END)
                    self.entry_field_platform.insert(0, self.selected_platform)

                    return True



    def get_selected_path(self):
        return self.current_iso_path

    def get_listbox(self):
        return self._listbox

    def get_ascending_index(self, list_of_items, item, ignore_case=True):
        lo = 0
        hi = len(list_of_items)

        if ignore_case:
            item = item.lower()
            while lo < hi:
                mid = (lo + hi) // 2

                if item < list_of_items[mid].lower():
                    hi = mid
                else:
                    lo = mid + 1
        else:
            while lo < hi:
                mid = (lo + hi) // 2

                if item < list_of_items[mid]:
                    hi = mid
                else:
                    lo = mid + 1
        return lo

    def add_item(self, item):
        if item != '':
            self.list_of_items = self._listbox.get(0, END)
            # getting ascending index in order to sort alphabetically
            index = self.get_ascending_index(self.list_of_items, item)

            self._listbox.insert(index, item)
        else:
            self._listbox.insert(END, item)

    def get_items(self):
        return self.list_of_items

    def _bound_to_mousewheel(self, event):
        self._listbox.bind_all("<MouseWheel>", self._on_mousewheel)

    def _unbound_to_mousewheel(self, event):
        self._listbox.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        self._listbox.yview_scroll(int(-1*(event.delta/30)), "units")

    def popup(self, event):
        try:
            self._listbox.selection_clear(0, END)
            self._listbox.selection_set(self._listbox.nearest(event.y))
            self._listbox.activate(self._listbox.nearest(event.y))
        finally:
            if self._listbox.get(self._listbox.curselection()[0]) is not '':
                self.popup_menu.tk_popup(event.x_root + 43, event.y_root + 12, 0)
                self.popup_menu.grab_release()
                self.popup_menu.focus_set()

    def delete_selected(self):
        import tkMessageBox
        game_folder_path = os.path.join(AppPaths.game_work_dir, '..')
        response = tkMessageBox.askyesno('Delete game folder', 'Delete \'' + self.entry_field_title.get() + '\'?\n\nFolder path: ' + os.path.realpath(game_folder_path))
        # yes
        if response:
            # remove game from visual game list
            for i in self._listbox.curselection()[::-1]:
                self._listbox.delete(i)
                removed_index = i

            # remove game from json game list
            platform_key = self.entry_field_platform.get() + '_games'
            self.json_game_list_data[platform_key] = [x for x in self.json_game_list_data[platform_key] if x['title'] != self.selected_title]

            # update the json game list file
            with open(GameListData.GAME_LIST_DATA_PATH, 'w') as newFile:
                json_text = json.dumps(self.json_game_list_data, indent=4, separators=(",", ":"))
                newFile.write(json_text)

            # remove the game build folder too
            if AppPaths.game_work_dir != os.path.join(AppPaths.wcm_gui, 'work_dir'):
                if os.path.isdir(game_folder_path):
                    if 'webman-classics-maker' in game_folder_path:
                        shutil.rmtree(game_folder_path)
                # clear entry_fields
                self.clear_entries_and_path()
                # set cursor
                self._listbox.select_set(removed_index) #This only sets focus on the first item.

    def rename_selected(self):
        self.entry_field_title.selection_range(0, END)
        self.entry_field_title.focus_set()

    def select_all(self):
        self._listbox.selection_set(0, 'end')


    def clear_entries_and_path(self):
        self.entry_field_title_id.delete(0, len(self.entry_field_title_id.get())-1)
        self.entry_field_title_id.delete(0, END)
        self.entry_field_title.delete(0, END)
        self.entry_field_platform.delete(0, END)
        self.entry_field_filename.delete(0, END)

        self.is_cleared = True



    def get_selected_build_dir_path(self):
        self.build_dir_path = ''
        if self.selected_filename not in {'', None}:
            filename = self.selected_filename
            title_id = self.selected_title_id.replace('-', '')
            build_base_path = AppPaths.builds

            tmp_filename = filename
            # removes the file extension from tmp_filename
            for file_ext in GlobalVar.file_extensions:
                if filename.upper().endswith(file_ext):
                    tmp_filename = filename[0:len(filename)-len(file_ext)]
                    break
            game_folder_name = tmp_filename.replace(' ', '_') + '_(' + title_id.replace('-', '') + ')'

            self.build_dir_path = os.path.join(build_base_path, game_folder_name)
        return self.build_dir_path

