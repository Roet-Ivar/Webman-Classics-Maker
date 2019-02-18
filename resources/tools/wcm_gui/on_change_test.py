import tkinter as tk
from tkinter import ttk

def generateOnChange(obj):
        obj.tk.eval('''
            proc widget_proxy {widget widget_command args} {

                # call the real tk widget command with the real args
                set result [uplevel [linsert $args 0 $widget_command]]

                # generate the event for certain types of commands
                if {([lindex $args 0] in {insert replace delete}) ||
                    ([lrange $args 0 2] == {mark set insert}) || 
                    ([lrange $args 0 1] == {xview moveto}) ||
                    ([lrange $args 0 1] == {xview scroll}) ||
                    ([lrange $args 0 1] == {yview moveto}) ||
                    ([lrange $args 0 1] == {yview scroll})} {

                    event generate  $widget <<Change>> -when tail
                }

                # return the result from the real widget command
                return $result
            }
            ''')
        obj.tk.eval('''
            rename {widget} _{widget}
            interp alias {{}} ::{widget} {{}} widget_proxy {widget} _{widget}
        '''.format(widget=str(obj)))

def onEntryChanged(event = None):
    print("Entry changed: " + entry.get())

def onCheckChanged(event = None):
    print("Check button changed")

def onSpinboxChanged(event = None):
    print("Spinbox changed")

def onRadioChanged(event = None):
    print("Radio changed")

if __name__ == '__main__':
    root = tk.Tk()

    frame = tk.Frame(root, width=400, height=400)

    entry = tk.Entry(frame, width=30)
    entry.grid(row=0, column=0)
    generateOnChange(entry)
    entry.bind('<<Change>>', onEntryChanged)

    checkbutton = tk.Checkbutton(frame, command=onCheckChanged)
    checkbutton.grid(row=1, column=0)

    spinbox = tk.Spinbox(frame, width=100, from_=1.0, to=100.0, command=onSpinboxChanged)
    spinbox.grid(row=2, column=0)


    phone = tk.StringVar()
    home = ttk.Radiobutton(frame, text='Home', variable=phone, value='home', command=onRadioChanged)
    home.grid(row=3, column=0, sticky=tk.W)
    office = ttk.Radiobutton(frame, text='Office', variable=phone, value='office', command=onRadioChanged)
    office.grid(row=3, column=0, sticky=tk.E)

    frame.pack()    
    root.mainloop()