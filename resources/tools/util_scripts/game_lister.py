import Tkinter
import json

class Gamelist():

	def create_window(self):
		self.F1 = Tkinter.Frame()
		s = Tkinter.Scrollbar(self.F1)
		self.L = Tkinter.Listbox(self.F1)

		s.pack(side=Tkinter.RIGHT, fill=Tkinter.Y)
		self.L.pack(side=Tkinter.LEFT, fill=Tkinter.Y)

		s['command'] = self.L.yview
		self.L['yscrollcommand'] = s.set


		with open('game_list_data.json') as f:
			json_game_list_data = json.load(f)

		for list_game in json_game_list_data['ps2_games']:
			self.L.insert(Tkinter.END, list_game['title'])

		self.F1.pack(side=Tkinter.TOP)

		self.F2 = Tkinter.Frame()
		self.lab = Tkinter.Label(self.F2)

	def poll(self):
		self.lab.after(200, self.poll)
		sel = self.L.curselection()
		self.lab.config(text=str(sel))

		self.lab.pack()
		self.F2.pack(side=Tkinter.TOP)
gl = Gamelist()
gl.create_window()
gl.poll()
Tkinter.mainloop()