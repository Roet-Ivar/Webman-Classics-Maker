from Tkinter import *
from tkFileDialog import askopenfile
from PIL import  Image,ImageTk


class GUI(Frame):

    def __init__(self, master=None):
        Frame.__init__(self, master)
        w,h = 650, 650
        master.minsize(width=w, height=h)
        master.maxsize(width=w, height=h)
        self.pack()

        self.file = Button(self, text='Browse', command=self.choose)
        self.choose = Label(self, text="Choose file").pack()
        #Replace with your image
        self.image = PhotoImage('ICON0.PNG')
        self.label = Label(image=self.image)


        self.file.pack()
        self.label.pack()

    def choose(self):
        ifile = askopenfile(parent=self,mode='rb',title='Choose a file')
        path = Image.open(ifile)

        self.image2 = ImageTk.PhotoImage(path)
        self.label.configure(image=self.image2)
        self.label.image=self.image2


root = Tk()
app = GUI(master=root)
app.mainloop()
root.destroy()