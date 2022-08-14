from tkinter import *

def sel():
   selection = "Value = " + str(var.get())
   label.config(text = selection)

root = Tk()
var = DoubleVar()
scale = Scale( root, variable = var , orient=HORIZONTAL, resolution=0.01, from_=0, to=(1442816-(1442816%1024))/1024/60)
scale.pack(anchor=CENTER, fill="both")

button = Button(root, text="Get Scale Value", command=sel)
button.pack(anchor=CENTER)

label = Label(root)
label.pack()

root.mainloop()