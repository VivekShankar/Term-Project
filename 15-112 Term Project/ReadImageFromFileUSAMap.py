# imagesDemo1.py
# view in canvas
# read from file
# with transparent pixels
# get size, resize (zoom and subsample)

# image resized, made transparent with:
# http://www.online-image-editor.com/

from Tkinter import *

def redrawAll(canvas):
    #canvas.delete(ALL)
    # Draw a background rectangle to highlight the transparency
    # of the images
    # Draw a double-size image on the right
    image = canvas.data["USAimage"]
    imageSize = ( (image.width(), image.height()) )
    msg = "Double-size " + str(imageSize)
    canvas.create_image(0,0, anchor=NW, image=image)

def init(canvas):
    canvas.width = canvas.winfo_reqwidth()-4
    canvas.height = canvas.winfo_reqheight()-4
    image = PhotoImage(file='usamapwithclouds1.gif')
    canvas.data["USAimage"] = image
    #halfImage = image.subsample(2,2)
    #canvas.data["halfImage"] = halfImage
    #doubleImage = image.zoom(3,3)
    #canvas.data["doubleImage"] = doubleImage
    redrawAll(canvas)

########### copy-paste below here ###########

def run(canvas):
    # create the root and the canvas
    canvas.data = { }
    init(canvas)
    # set up events
    # root.bind("<Button-1>", leftMousePressed)
    # root.bind("<KeyPress>", keyPressed)
    # timerFired(canvas)
    # and launch the app
    #root.mainloop()  # This call BLOCKS (so your program waits until you close the window!)
