import tkinter as tk
# from PIL import Image, ImageTk
from itertools import count, cycle
from decimal import *

class ImageLabel(tk.Label):

	def load(self, im):
		if isinstance(im, str):
			# im = Image.open(im)
			im = tk.PhotoImage(file='redish_opt.gif')
		frames = []

		try:
			i = 0
			while i < 134:
				percent = int(i/134*100)
				print('Loading gif: ' + str(percent) + '%')
				frames.append(tk.PhotoImage(file='redish_opt.gif', format='gif -index {}'.format(i)))
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
lbl.load('ball-small.gif')
root.mainloop()