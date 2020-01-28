from Tkinter import Frame, Scrollbar, Listbox, LEFT, RIGHT, Y, END, Label
import json, os, sys
from shutil import copyfile
sys.path.append('..')
from global_paths import App as AppPaths



class Gamelist():

    def __init__(self, platform):
        # makes sure there is a json_game_list file
        if os.path.isfile(os.path.join(AppPaths.util_scripts, 'game_list_data.json')) is False:
            copyfile(os.path.join(AppPaths.util_resources, 'game_list_data.json.BAK'), os.path.join(AppPaths.util_scripts, 'game_list_data.json'))

        self.platform_to_show = platform.lower() + '_games'

        with open(os.path.join(AppPaths.util_scripts, 'game_list_data.json')) as f:
            self.json_game_list_data = json.load(f)


        print('platform_to_show: ' + self.platform_to_show)
        self.WCM_BASE_PATH  = AppPaths.wcm_gui
        self.last_selection = (None, 0)
        self.list_of_items = []


    def create_main_frame(self, entry_field_title_id, entry_field_title, entry_field_filename, entry_field_iso_path, drive_system_array):
        self.entry_field_title_id   = entry_field_title_id
        self.entry_field_title      = entry_field_title
        self.entry_field_filename   = entry_field_filename
        self.entry_field_iso_path   = entry_field_iso_path
        self.drive_system_array     = drive_system_array


        self.corrected_index = []
        self.main_frame = Frame()
        s = Scrollbar(self.main_frame)
        self._listbox = Listbox(self.main_frame, width=465)

        s.pack(side=RIGHT, fill=Y)
        self._listbox.pack(side=LEFT, fill=Y)

        s['command'] = self._listbox.yview
        self._listbox['yscrollcommand'] = s.set


        if 'all_games' == self.platform_to_show:
            for platform in self.json_game_list_data:
                for list_game in self.json_game_list_data[platform]:
                    self.add_item(list_game['title'])

        else:
            for list_game in self.json_game_list_data[self.platform_to_show]:
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
        # cursor har been initiated
        if self._listbox.curselection() is not ():
            new_selection = self._listbox.curselection()
            if new_selection[0] is not self.last_selection[0]:
                self.entry_fields_update(new_selection)

            self.last_selection = new_selection

    def entry_fields_update(self, new_selection):
        for platform in self.json_game_list_data:
            for list_game in self.json_game_list_data[platform]:
                selected_title = self._listbox.get(new_selection[0])
                tmp_title = list_game['title']
                if selected_title == str(tmp_title):
                    selected_title_id   = str(list_game['title_id'])
                    selected_title      = str(list_game['title'])
                    selected_path       = str(list_game['path'])
                    selected_filename   = str(list_game['filename'])

                    # parse drive and system from json data
                    path_array = filter(None, selected_path.split('/'))
                    self.drive_system_array[0] = path_array[0]
                    self.drive_system_array[1] = path_array[1]

                    self.entry_field_title_id.delete(0, END)
                    self.entry_field_title_id.insert(0, selected_title_id.replace('-', ''))

                    self.entry_field_title.delete(0, END)
                    self.entry_field_title.insert(0, selected_title)

                    self.entry_field_filename.delete(0, END)
                    self.entry_field_filename.insert(0, selected_filename)

                    break


    def get_selected_path(self):
        return self.current_iso_path

    def get_listbox(self):
        return self._listbox

    def get_ascending_index(self, list_of_items, item, ignore_case=False):
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

    # TODO: not used yet
    def load_pkg_project(self, title_id, filename):
        _filename = filename.replace(' ', '_')
        build_base_path = os.path.join(AppPaths.builds, 'builds')
        pkg_project_name = title_id + '_' + _filename[:-4]

        build_dir_path = os.path.join(build_base_path, pkg_project_name)
        if os.path.exists(build_dir_path):
            print(_filename + ' project exist')