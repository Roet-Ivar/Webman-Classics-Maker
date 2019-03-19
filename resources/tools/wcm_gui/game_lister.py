import Tkinter
from Tkinter import Frame, Scrollbar, Listbox, LEFT, RIGHT, Y, END, TOP, Label
import json

class Gamelist():

	def start(self, ):
		self.create_window()
		return self.F1


	def create_window(self):
		self.F1 = Frame()
		s = Scrollbar(self.F1)
		self._listbox = Listbox(self.F1, width=385)

		s.pack(side=RIGHT, fill=Y)
		self._listbox.pack(side=LEFT, fill=Y)

		s['command'] = self._listbox.yview
		self._listbox['yscrollcommand'] = s.set

		with open('../util_scripts/game_list_data.json') as f:
			json_game_list_data = json.load(f)

		for list_game in json_game_list_data['ps2_games']:

			self.add_item(list_game['title'])

		# self.F1.pack(side=TOP)

		self.F2 = Frame()
		self.lab = Label(self.F2)

		self.poll()



	def poll(self):
		# print('poll')
		self.lab.after(200, self.poll)
		sel = self._listbox.curselection()
		self.lab.config(text=str(sel), width=385)
		self.lab.pack()

	def get_game_list(self):
		return self._listbox

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