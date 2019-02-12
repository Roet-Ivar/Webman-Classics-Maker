import tkinter as tk
# from PIL import Image, ImageTk
from itertools import count, cycle

class ImageLabel(tk.Label):

	def load(self, im):
		if isinstance(im, str):
			# im = Image.open(im)
			im = tk.PhotoImage(file='continues_249.gif')
		frames = []

		try:
			for i in range(0,248):
				frames.append(tk.PhotoImage(file='continues_249.gif', format='gif -index {}'.format(i)))
		except EOFError:
			pass
		self.frames = cycle(frames)

		try:
			self.delay = 50
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

root = tk.Tk()
lbl = ImageLabel(root)
lbl.pack()
lbl.load('ball-small.gif')
root.mainloop()