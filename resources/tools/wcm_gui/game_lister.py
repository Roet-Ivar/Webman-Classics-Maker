import Tkinter
from Tkinter import Frame, Scrollbar, Listbox, LEFT, RIGHT, Y, END, TOP, Label
import json


class Gamelist():

    def __init__(self, ref_title_id, ref_title, ref_filename):
        self.entry_title_id = ref_title_id
        self.entry_title    = ref_title
        self.entry_filename = ref_filename

        self.last_selection = (None, 0)
        self.platform = 'ps2'


    def start(self):
        self.create_main_frame()
        return self.main_frame

    def create_main_frame(self):
        self.corrected_index = []
        self.main_frame = Frame()
        s = Scrollbar(self.main_frame)
        self._listbox = Listbox(self.main_frame, width=1000)

        s.pack(side=RIGHT, fill=Y)
        self._listbox.pack(side=LEFT, fill=Y)

        s['command'] = self._listbox.yview
        self._listbox['yscrollcommand'] = s.set

        with open('../util_scripts/game_list_data.json') as f:
            self.json_game_list_data = json.load(f)

        for list_game in self.json_game_list_data[self.platform + '_games']:
            self.add_item(list_game['title'])


        self.label = Label(self.main_frame)
        self.cursor_poller()

    def cursor_poller(self):
        self.label.after(200, self.cursor_poller)
        # cursor har been initiated
        if self._listbox.curselection() is not ():
            new_selection = self._listbox.curselection()
            if new_selection[0] is not self.last_selection[0]:
                for list_game in self.json_game_list_data[self.platform + '_games']:
                    selected_title = self._listbox.get(new_selection[0])
                    tmp_title = list_game['title']
                    if selected_title == str(tmp_title):
                        selected_title_id   = str(list_game['title_id'])
                        selected_title      = str(list_game['title'])
                        selected_filename   = str(list_game['filename'])

                        self.entry_title_id.delete(0, END)
                        self.entry_title_id.insert(0, selected_title_id.replace('-', ''))

                        self.entry_title.delete(0, END)
                        self.entry_title.insert(0, selected_title)

                        self.entry_filename.delete(0, END)
                        self.entry_filename.insert(0, selected_filename)

                        break
            self.last_selection = new_selection

    def get_game_listbox(self):
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
        self.list_of_items = self._listbox.get(0, END)
        # getting ascending index in order to sort alphabetically
        index = self.get_ascending_index(self.list_of_items, item)
        self._listbox.insert(index, item)

    def get_game_list(self):
        return self.list_of_items
