import Tkinter
from Tkinter import Frame, Scrollbar, Listbox, LEFT, RIGHT, Y, END, TOP, Label
import json


class Gamelist():
    def __init__(self, ref_title_id, ref_title, ref_filename):
        self.entry_title_id     = ref_title_id
        self.entry_title        = ref_title
        self.entry_filename     = ref_filename

        self.sel = ()
        self.tmp_sel = ()


    def start(self):
        self.create_window()
        return self.F1

    def create_window(self):
        self.corrected_index = []
        self.F1 = Frame()
        s = Scrollbar(self.F1)
        self._listbox = Listbox(self.F1, width=1000)

        s.pack(side=RIGHT, fill=Y)
        self._listbox.pack(side=LEFT, fill=Y)

        s['command'] = self._listbox.yview
        self._listbox['yscrollcommand'] = s.set

        with open('../util_scripts/game_list_data.json') as f:
            self.json_game_list_data = json.load(f)

        for list_game in self.json_game_list_data['ps2_games']:
            self.add_item(list_game['title'])

        self.F2 = Frame()
        self.label = Label(self.F2)
        self.poll()

    def poll(self):
        self.label.after(200, self.poll)

        self.sel = self._listbox.curselection()
        print('sel: ' + str(self.sel) + ' vs tmp_sel: ' + str(self.tmp_sel))
        if self.sel is not () and self.tmp_sel is not ():
            if self.sel[0] is not self.tmp_sel[0]:
                print('sel is not tmp_sel')
                for list_game in self.json_game_list_data['ps2_games']:
                    s = self._listbox.get(self.sel[0])
                    if s in str(list_game['title']):
                        # print(str(list_game['title_id']))
                        selected_title_id       = str(list_game['title_id'])
                        selected_title          = str(list_game['title'])
                        selected_filename       = str(list_game['filename'])

                        self.entry_title_id.delete(0, END)
                        self.entry_title_id.insert(0, selected_title_id.replace('-', ''))

                        self.entry_title.delete(0, END)
                        self.entry_title.insert(0, selected_title)

                        self.entry_filename.delete(0, END)
                        self.entry_filename.insert(0, selected_filename)

                        break
        self.tmp_sel = self._listbox.curselection()

    def get_game_listbox(self):
        return self._listbox

    def get_corrected_index(self):
        return self.corrected_index

    def bisect(self, list_of_items, item, ascending_order=True, ignore_case=False):
        lo = 0
        hi = len(list_of_items)

        # I repeat a little bit myself here because I want to be more efficient.
        if ascending_order:
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
        else:
            if ignore_case:
                item = item.lower()
                while lo < hi:
                    mid = (lo + hi) // 2

                    if item > list_of_items[mid].lower():
                        hi = mid
                    else:
                        lo = mid + 1
            else:
                while lo < hi:
                    mid = (lo + hi) // 2

                    if item > list_of_items[mid]:
                        hi = mid
                    else:
                        lo = mid + 1
        return lo

    def add_item(self, item):
        list_of_items = self._listbox.get(0, END)
        index = self.bisect(list_of_items, item)
        self._listbox.insert(index, item)
        # print('index: ' + str(index) + ' & item: ' + str(item))

    def get_json_index_of_title(self, title):
        return self._listbox.get(0, "end").index(title)