
from Tkinter import *
import urllib
import os


from StringIO import StringIO


 
 """
 I have  a file locally called "test9.gif"
 """   
    
def redrawAll(canvas):
    canvas.delete(ALL)
    image = canvas.data["image"]
    halfimage = image.subsample(2,2)
    canvas.create_image(canvas.width/2, 0, anchor=N, image=halfimage)

def timerFired(canvas):
    redrawAll(canvas)
    delay = 1000 # milliseconds
    canvas.after(delay, timerFired, canvas)

def init(canvas):
    canvas.width = canvas.winfo_reqwidth()-4
    canvas.height = canvas.winfo_reqheight()-4
    image = PhotoImage(file="test9.gif")
    canvas.data["image"] = image
    halfimage = image.subsample(2,2)
    canvas.create_image(canvas.width/5, 100, anchor=N, image=halfimage)
    redrawAll(canvas)

def run():
    # create the root and the canvas
    root = Tk()
    root.resizable(width=FALSE, height=FALSE)
    canvas = Canvas(root, width=500, height=500)
    canvas.pack(fill=BOTH, expand=YES)
    # Store canvas in root and in canvas itself for callbacks
    root.canvas = canvas.canvas = canvas
    # Set up canvas data and call init
    canvas.data = { }
    init(canvas)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    # root.bind("<KeyPress>", keyPressed)
    timerFired(canvas)
    # and launch the app
    root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)

run()