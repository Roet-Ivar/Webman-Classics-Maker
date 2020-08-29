import Tkinter as tk
# from PIL import Image, ImageTk
from itertools import count, cycle
from decimal import *

class ImageLabel(tk.Label):

	def load(self, im):
		if isinstance(im, str):
			# im = Image.open(im)
			im = tk.PhotoImage(file='window_55f_opt.gif')
		frames = []

		try:
			total_frames = 55
			i = 1
			while i < total_frames:
				percent = int(100*i/total_frames)
				print('Loading gif: ' + str(percent) + '%')
				frames.append(tk.PhotoImage(file='window_55f_opt.gif', format='gif -index {}'.format(i)))
				i += 1


		except EOFError:
			pass
		self.frames = cycle(frames)

		try:
			self.delay = 40
		except:
			self.delay = 100

		if len(frames) == 1:
			self.config(image=next(self.frames))
		else:
			self.next_frame()

	def unload(self):
		self.config(image=None)
		self.frames = None

	def next_frame(self):
		if self.frames:
			self.config(image=next(self.frames))
			self.after(self.delay, self.next_frame)
		else:
			self.unload()

root = tk.Tk()
lbl = ImageLabel(root)
lbl.pack()
lbl.load('window_55f_opt.gif')
root.mainloop()