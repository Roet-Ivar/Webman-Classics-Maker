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
		self.list = Listbox(self.F1, width=385)

		s.pack(side=RIGHT, fill=Y)
		self.list.pack(side=LEFT, fill=Y)

		s['command'] = self.list.yview
		self.list['yscrollcommand'] = s.set

		with open('../util_scripts/game_list_data.json') as f:
			json_game_list_data = json.load(f)

		for list_game in json_game_list_data['ps2_games']:
			self.list.insert(END, list_game['title'])

		# self.F1.pack(side=TOP)

		self.F2 = Frame()
		self.lab = Label(self.F2)

		self.poll()



	def poll(self):
		# print('poll')
		self.lab.after(200, self.poll)
		sel = self.list.curselection()
		self.lab.config(text=str(sel), width=385)
		self.lab.pack()

	def get_game_list(self):
		return self.list