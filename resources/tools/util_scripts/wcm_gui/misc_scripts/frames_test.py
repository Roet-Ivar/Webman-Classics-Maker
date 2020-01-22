from tkinter import *
from tkinter import ttk

root = Tk()
root.title('Example of Tkinter module')

main_window_width=1000
main_window_height=600
root.geometry('{}x{}'.format((main_window_width), str(main_window_height)) )


frame_top    			= Frame(root, width=main_window_width, height=50, bg="")
frame_bottom   		= Frame(root, width=main_window_width, height=50, bg="")

frame_middle_row 		= Frame(root, bg="")
frame_middle_row_left	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-50, bg="#000fff000")
frame_middle_row_right	= Frame(frame_middle_row, width=main_window_width, height=main_window_height-50, bg="#000ffffff")


root.grid_rowconfigure(1,weight=1)
root.grid_columnconfigure(0,weight=1)


frame_top.grid(row=0,sticky="ew")
frame_bottom.grid(row=2,sticky="ew")
frame_middle_row.grid(row=1,sticky="ew")

frame_middle_row_left.grid(row=0, column=0,sticky="w", in_=frame_middle_row)
frame_middle_row_right.grid(row=0, column=1,sticky="e", in_=frame_middle_row)


frame_middle_row.grid_columnconfigure(0,weight=2)
frame_middle_row.grid_columnconfigure(1,weight=1)
frame_top.grid_columnconfigure(0,weight=1)


# label_1 = Label(frame_top, text="text label",bg="#154e72")
#label_1.grid(sticky="w")


root.resizable(width=FALSE, height=FALSE)
root.mainloop()